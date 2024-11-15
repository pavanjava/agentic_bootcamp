from abc import ABC

from llama32_model import Llama32
from phi35_model import Phi35
import litserve as ls


class Phi35Vision(ls.LitAPI, ABC):
    def __init__(self):
        self.phi35model: Phi35 = None
        self.llama32model: Llama32 = None
        self.model: str = ''

    def setup(self, device):
        self.phi35model = Phi35(device)
        self.llama32model = Llama32(device)

    def decode_request(self, request):
        self.model = request.model
        if self.model == 'phi-vision':
            return self.phi35model.apply_chat_template(messages=request.messages)
        elif self.model == 'llama-vision':
            return self.llama32model.apply_chat_template(messages=request.messages)

    def predict(self, inputs, context):
        if self.model == 'llama-vision':
            yield self.llama32model(inputs=inputs)
        if self.model == 'phi-vision':
            yield self.phi35model(inputs=inputs)

    def encode_response(self, outputs):
        for output in outputs:
            if self.model == 'llama-vision':
                yield {"role": "assistant", "content": self.llama32model.decode_tokens(output)}
            if self.model == 'phi-vision':
                yield {"role": "assistant", "content": self.phi35model.decode_tokens(output)}


if __name__ == "__main__":
    api = Phi35Vision()
    server = ls.LitServer(api, spec=ls.OpenAISpec())
    server.run(port=8000)
