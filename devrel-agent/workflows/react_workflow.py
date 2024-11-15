import os
from typing import Any
from llama_index.core import Settings
from llama_index.core.agent.react import ReActChatFormatter, ReActOutputParser
from llama_index.core.agent.react.types import (
    ActionReasoningStep,
    ObservationReasoningStep,
)
from llama_index.core.base.llms.types import ChatMessage
from llama_index.core.llms.llm import LLM, ToolSelection
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.tools import FunctionTool
from llama_index.core.tools.types import BaseTool
from llama_index.core.workflow import (
    Context,
    Workflow,
    StartEvent,
    StopEvent,
    step,
)
from llama_index.llms.ollama import Ollama
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

from workflows.events.events import ContinueEvent, ToolCallEvent, InputEvent
from workflows.tools.tools import post_to_linkedin, burn_story_in_jira, create_terraform_code, create_k8s_code

import uuid


class ReActAgentWorkflow(Workflow):
    def __init__(
            self,
            *args: Any,
            llm: LLM | None = None,
            tools: list[BaseTool] | None = None,
            extra_context: str | None = None,
            **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.tools = tools or []

        Settings.embed_model = OpenAIEmbedding(model=os.environ.get('OPENAI_EMBED_MODEL'))
        self.llm = llm or OpenAI()

        self.memory = ChatMemoryBuffer.from_defaults(llm=llm)

        self.formatter = ReActChatFormatter(context=extra_context or "")
        self.output_parser = ReActOutputParser()
        self.sources = []

    @step
    async def new_user_msg(self, ctx: Context, ev: StartEvent) -> ContinueEvent:
        # clear sources
        self.sources = []

        # system prompt
        self.memory.put(ChatMessage(role="system", content=ev.system_prompt))

        # get user input
        user_input = ev.input
        user_msg = ChatMessage(role="user", content=user_input)
        self.memory.put(user_msg)

        # clear current reasoning
        await ctx.set("current_reasoning", [])

        return ContinueEvent()

    @step
    async def prepare_chat_history(self, ctx: Context, ev: ContinueEvent) -> InputEvent:
        # get chat history
        chat_history = self.memory.get()
        current_reasoning = await ctx.get("current_reasoning", default=[])
        llm_input = self.formatter.format(
            self.tools, chat_history, current_reasoning=current_reasoning
        )
        return InputEvent(input=llm_input)

    @step
    async def handle_llm_input(self, ctx: Context, ev: InputEvent) -> ToolCallEvent | StopEvent:
        chat_history = ev.input

        response = await self.llm.achat(chat_history)

        try:
            reasoning_step = self.output_parser.parse(response.message.content)
            (await ctx.get("current_reasoning", default=[])).append(
                reasoning_step
            )
            if reasoning_step.is_done:
                self.memory.put(
                    ChatMessage(
                        role="assistant", content=reasoning_step.response
                    )
                )
                return StopEvent(
                    result={
                        "response": reasoning_step.response,
                        "sources": [*self.sources],
                        "reasoning": await ctx.get(
                            "current_reasoning", default=[]
                        )
                    }
                )
            elif isinstance(reasoning_step, ActionReasoningStep):
                tool_name = reasoning_step.action
                tool_args = reasoning_step.action_input
                return ToolCallEvent(
                    tool_calls=[
                        ToolSelection(
                            tool_id=str(uuid.uuid4()),
                            tool_name=tool_name,
                            tool_kwargs=tool_args,
                        )
                    ]
                )
        except Exception as e:
            (await ctx.get("current_reasoning", default=[])).append(
                ObservationReasoningStep(
                    observation=f"There was an error in parsing my reasoning: {e}"
                )
            )

        # if no tool calls or final response, iterate again
        return ContinueEvent()

    @step
    async def handle_tool_calls(self, ctx: Context, ev: ToolCallEvent) -> ContinueEvent:
        tool_calls = ev.tool_calls
        tools_by_name = {tool.metadata.get_name(): tool for tool in self.tools}

        # call tools -- safely!
        for tool_call in tool_calls:
            tool = tools_by_name.get(tool_call.tool_name)
            if not tool:
                (await ctx.get("current_reasoning", default=[])).append(
                    ObservationReasoningStep(
                        observation=f"Tool {tool_call.tool_name} does not exist"
                    )
                )
                continue

            try:
                tool_output = tool(**tool_call.tool_kwargs)
                self.sources.append(tool_output)
                (await ctx.get("current_reasoning", default=[])).append(
                    ObservationReasoningStep(observation=tool_output.content)
                )
            except Exception as e:
                (await ctx.get("current_reasoning", default=[])).append(
                    ObservationReasoningStep(
                        observation=f"Error calling tool {tool.metadata.get_name()}: {e}"
                    )
                )

        # prep the next iteraiton
        return ContinueEvent()


def build_react_agent_workflow() -> ReActAgentWorkflow:
    tools = [
        FunctionTool.from_defaults(fn=post_to_linkedin),
        FunctionTool.from_defaults(fn=burn_story_in_jira),
        FunctionTool.from_defaults(fn=create_terraform_code),
        FunctionTool.from_defaults(fn=create_k8s_code)
    ]

    agent = ReActAgentWorkflow(
        llm=OpenAI(model=os.environ.get('OPENAI_MODEL'), temperature=0.3), tools=tools, timeout=120, verbose=True
    )

    return agent
