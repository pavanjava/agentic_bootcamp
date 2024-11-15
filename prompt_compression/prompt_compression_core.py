from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from llmlingua import PromptCompressor

# Initialize the FastAPI app
app = FastAPI()


# Define the request and response models
class CompressionRequest(BaseModel):
    # microsoft/llmlingua-2-xlm-roberta-large-meetingbank,
    # microsoft/llmlingua-2-bert-base-multilingual-cased-meetingbank
    model_name: str
    original_prompt: str
    rate: Optional[float] = 0.6  # Default compression rate


class CompressionResponse(BaseModel):
    original_prompt: str
    compressed_prompt: str
    original_tokens: int
    compressed_tokens: int
    compression_rate: str


@app.post("/compress_prompt", response_model=CompressionResponse)
def compress_prompt(request: CompressionRequest):
    try:
        # Initialize the PromptCompressor with the specified model
        compressor = PromptCompressor(
            model_name=request.model_name,
            use_llmlingua2=True,
            device_map="cpu"
        )

        # Perform the compression
        results = compressor.compress_prompt_llmlingua2(
            [request.original_prompt],
            rate=float(request.rate),
            force_tokens=['\n', '.', '!', '?', ','],
            chunk_end_tokens=['.', '\n'],
            return_word_label=True,
            drop_consecutive=True
        )

        # Return the response in JSON format
        return {
            "original_prompt": request.original_prompt,
            "compressed_prompt": results['compressed_prompt'],
            "original_tokens": results['origin_tokens'],
            "compressed_tokens": results['compressed_tokens'],
            "compression_rate": results['rate']
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("prompt_compression_core:app", host="0.0.0.0", port=8000, reload=True)
