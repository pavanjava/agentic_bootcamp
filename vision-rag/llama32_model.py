import os

from transformers import MllamaForConditionalGeneration, AutoProcessor
from litserve.specs.openai import ChatMessage
from huggingface_hub import login
from dotenv import load_dotenv, find_dotenv
import torch
from typing import List

from utils import decode_base64_image

load_dotenv(find_dotenv())


class Llama32:
    def __init__(self, device):
        login(token=os.environ.get("HF_TOKEN"))
        model_id = "meta-llama/Llama-3.2-11B-Vision-Instruct"

        self.model = MllamaForConditionalGeneration.from_pretrained(model_id, torch_dtype=torch.bfloat16,
                                                                    device_map=device)
        self.processor = AutoProcessor.from_pretrained(model_id)
        self.device = device

    def apply_chat_template(self, messages: List[ChatMessage]):
        final_messages = []
        image = None
        for message in messages:
            msg = {}
            if message.role == "system":
                msg["role"] = "system"
                msg["content"] = message.content
            elif message.role == "user":
                msg["role"] = "user"
                content = message.content
                final_content = []
                if isinstance(content, list):
                    for i, content in enumerate(content):
                        if content.type == "text":
                            final_content.append(content.dict())
                        elif content.type == "image_url":
                            url = content.image_url.url
                            image = decode_base64_image(url)
                            final_content.append({"type": "image"})
                    msg["content"] = final_content
                else:
                    msg["content"] = content
            elif message.role == "assistant":
                content = message.content
                msg["role"] = "assistant"
                msg["content"] = content
            final_messages.append(msg)
        prompt = self.processor.apply_chat_template(
            final_messages, tokenize=False, add_generation_prompt=True
        )
        return prompt, image

    def __call__(self, inputs):
        prompt, image = inputs
        inputs = self.processor(image, prompt, return_tensors="pt").to(self.model.device)
        generation_args = {
            "max_new_tokens": 1000,
            "temperature": 0.2,
            "do_sample": False,
        }

        generate_ids = self.model.generate(
            **inputs,
            **generation_args,
        )
        return inputs, generate_ids

    def decode_tokens(self, outputs):
        inputs, generate_ids = outputs
        generate_ids = generate_ids[:, inputs["input_ids"].shape[1]:]
        response = \
            self.processor.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
        return response
