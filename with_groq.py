import os
import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

# Initialize FastAPI application
app = FastAPI()

# Load variables from .env file
load_dotenv()

# Configuration: (Keep your requested setup)
#  SECURE: Reads from the file instead of leaking it in the code
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Input validation schema
class PromptRequest(BaseModel):
    prompt: str = Field(..., description="The core text prompt for the AI.")
    tone: str = Field(default="professional", description="The tone of the response: friendly, professional, humorous, neutral.")

# Global exception handler for malformed client JSON payloads
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": "Unprocessable Entity",
            "message": "Your JSON request structure or syntax is invalid. Check for unescaped newlines or hidden formatting control characters.",
            "details": exc.errors()
        }
    )

@app.post("/generate-text", summary="Generate toned text using Groq LLM")
def generate_text(request: PromptRequest):
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt string cannot be empty or just whitespace.")
        
    # Map tones to internal prompt behavior adjustments
    tone_prefix = {
        "friendly": "Hey there! ",
        "professional": "Dear Sir/Madam, ",
        "humorous": "Here's a joke for you: ",
        "neutral": ""
    }.get(request.tone.lower(), "")
    
    # Construct final prompt string
    final_prompt = tone_prefix + request.prompt
    
    # Kept exactly as requested
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        # FIXED: Updated decommissioned llama3-8b-8192 to the active equivalent model
        "model": "llama-3.1-8b-instant",
        "messages": [
            {
                "role": "system", 
                "content": f"You are a helpful assistant that responds precisely in a {request.tone} tone."
            },
            {
                "role": "user", 
                "content": final_prompt
            }
        ],
        "max_tokens": 150
    }
    
    try:
        # Route network request to upstream Groq cluster
        response = requests.post(url, headers=headers, json=payload, timeout=30.0)
        
        # Explicit error reporting if credentials or payloads fail upstream
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code, 
                detail=f"Groq API upstream failure (Status {response.status_code}): {response.text}"
            )
            
        data = response.json()
        
        # FIXED: Uses list index [0] to extract accurately from the choices block
        generated_text = data['choices'][0]['message']['content']
        
        return {
            "tone_used": request.tone,
            "generated_text": generated_text,
            "survey": "completed"
        }
        
    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="Gateway Timeout: Request to Groq API timed out.")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Internal connection failure: {str(e)}")
