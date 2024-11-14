#!/usr/bin/env python
from fastapi import APIRouter
from fastapi import FastAPI

from langchain_helper import generate_itinerary
from model import Itinerary

router = APIRouter()


@router.post("/itinerary")
async def generate_itinerary_endpoint(itinerary_request: dict) -> Itinerary:
    destination = itinerary_request['destination']
    traveller_info = itinerary_request['traveller_info']
    return generate_itinerary(destination, traveller_info)


app = FastAPI(
  title="LangChain Server",
  version="1.0",
  description="A simple API server using LangChain's Runnable interfaces",
)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)