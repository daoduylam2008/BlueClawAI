from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi import FastAPI, status

import subprocess

import utils
import logging

from dotenv import load_dotenv


load_dotenv()
# Define the environment for networking call
subprocess.run("export USER_AGENT=USER_AGENT", shell=True)

models = {}

logger = logging.getLogger('uvicorn.error')

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager to load and clear the models.
    """
    import llm
    logger.info("Loading LLM model to the server.")
    models["llm"] = llm.LLM()

    yield
    logger.info("Clearing models.")
    models.clear()

app = FastAPI(lifespan=lifespan)

@app.get("/request/")
async def request(query: str):
    """
    Request to run the llm model.
    """
    responses = models['llm'].request(query)

    ai_response = utils.ai_sort(responses)[-1]
    tool_response = utils.tool_sort(responses)[-1]
    human_response = utils.human_sort(responses)[-1]

    content = {
        "ai_response": str(ai_response.content),
        "tool_response": str(tool_response.tool_calls),
        "human_response": str(human_response.content)
    }
    print(1)
    return JSONResponse(media_type="application/json", status_code=status.HTTP_200_OK, content=content)

@app.get("/")
async def root():
    """
    Root endpoint to return a message.
    """
    return {"message": "Hello World"}
