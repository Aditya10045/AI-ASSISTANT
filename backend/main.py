from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI()

# Allow all frontend origins (adjust for security if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    prompt: str

@app.post("/generate")
def generate_response(data: PromptRequest):
    try:
        res = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "tinyllama",
                "prompt": data.prompt,
                "stream": False
            }
        )
        response_text = res.json()["response"].strip()
        return {"response": response_text}
    except Exception as e:
        return {"error": str(e)}
