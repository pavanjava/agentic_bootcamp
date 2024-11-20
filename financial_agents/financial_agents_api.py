import litserve as ls

from introspective_agents import StockDataRetrieverTool, FinancialAgentBuilder


class FinancialAgentsAPI(ls.LitAPI):
    def __init__(self):
        # Instantiate tool and agent
        self.stock_data_tool = StockDataRetrieverTool()
        self.financial_agent_builder = None

    def setup(self, device):
        self.financial_agent_builder = FinancialAgentBuilder(data_tool=self.stock_data_tool)

    def decode_request(self, request, **kwargs):
        return request["query"]

    def predict(self, x, **kwargs):
        introspective_agent = self.financial_agent_builder.create_introspective_agent(verbose=True)
        response = introspective_agent.chat(x)
        return response

    def encode_response(self, output, **kwargs):
        return {"agent": output}


if __name__ == "__main__":
    api = FinancialAgentsAPI()
    server = ls.LitServer(api, accelerator="auto")
    server.run(port=8002)