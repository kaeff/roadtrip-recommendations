#!/usr/bin/env python
from fastapi import FastAPI
from langserve import add_routes

from langchain_helper import make_chain

chain = make_chain()

app = FastAPI(
  title="LangChain Server",
  version="1.0",
  description="A simple API server using LangChain's Runnable interfaces",
)

add_routes(
    app,
    chain,
    path="/chain",
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)