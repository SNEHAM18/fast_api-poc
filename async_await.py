from fastapi import FastAPI
import httpx
import time
import asyncio

app = FastAPI()

joke_url = "https://official-joke-api.appspot.com/random_joke"

@app.get("/sync-jokes")
def fetch_sync_jokes():  # Renamed
    start_time = time.time()
    jokes = []
    with httpx.Client() as client:
        for i in range(10):
            response = client.get(joke_url)
            data = response.json()
            # Safe dict access with defaults
            setup = data.get('setup', 'No setup found')
            punchline = data.get('punchline', 'No punchline found')
            jokes.append(f"{setup} - {punchline}")

    elapsed_time = time.time() - start_time
    return {
        "mode": "Synchronous",
        "jokes": jokes,
        "elapsed_time": elapsed_time
    }


@app.get("/async-jokes1")
async def fetch_async_jokes_sequential():  # Renamed
    start_time = time.time()
    jokes = []
    async with httpx.AsyncClient() as client:
        for i in range(10):
            response = await client.get(joke_url)
            data = response.json()
            setup = data.get('setup', 'No setup found')
            punchline = data.get('punchline', 'No punchline found')
            jokes.append(f"{setup} - {punchline}")
            
    elapsed_time = time.time() - start_time
    return {
        "mode": "Asynchronous",
        "jokes": jokes,
        "elapsed_time": elapsed_time
    }


@app.get("/async-jokes2")
async def fetch_async_jokes_concurrent():  # Renamed
    start_time = time.time()
    jokes = []
    async with httpx.AsyncClient() as client:
        # Removed the outer 'for i in range(10)' loop
        tasks = [client.get(joke_url) for _ in range(10)]
        responses = await asyncio.gather(*tasks)
        
        for response in responses:
            data = response.json()
            setup = data.get('setup', 'No setup found')
            punchline = data.get('punchline', 'No punchline found')
            jokes.append(f"{setup} - {punchline}")

    elapsed_time = time.time() - start_time
    return {
        "mode": "Asynchronous with gather",
        "jokes": jokes,
        "elapsed_time": elapsed_time
    }
