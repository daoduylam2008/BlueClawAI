from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi import FastAPI, status

import utils
import logging


models = {}
setting = {}

logger = logging.getLogger('uvicorn.error')

@asynccontextmanager
async def lifespan(app: FastAPI):
    import llm
    logger.info("Loading LLM model to the server...")
    models["llm"] = llm.LLM(0)

    yield
    print("Clear models")
    models.clear()

app = FastAPI(lifespan=lifespan)

@app.get("/request/")
async def instruction(query: str, model='llm'):
    responses = models[model].request(query)

    ai_response = utils.ai_sort(responses)[0]
    tool_response = utils.tool_sort(responses)[0]
    human_response = utils.human_sort(responses)[0]

    content = {
        "ai_response": str(ai_response.content),
        "tool_response": str(tool_response.tool_calls),
        "human_response": str(human_response.content)
    }
    return JSONResponse(status_code=status.HTTP_200_OK, content=content)

