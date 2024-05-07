from fastapi import FastAPI

app = FastAPI()

def say(something : str) -> dict:
    return {"msg": something}

@app.get("/")
async def read_main():
    return say("Hello World") 
