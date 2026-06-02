from fastapi import FastAPI
from config import settings
app=FastAPI()

@app.get("/std_env")
def read_env():
    return {
        "GROQ_API_KEY": settings.GROQ_API_KEY,
        "test_open_api_key": settings.test_open_api_key,
        "test_database_url": settings.test_database_url,
        "test_debug": settings.test_debug
    }