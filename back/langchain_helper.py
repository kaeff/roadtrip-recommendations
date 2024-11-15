import os

from langchain_core.messages import AIMessage, BaseMessage
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_openai import ChatOpenAI
from openai import BaseModel
from pydantic import BaseModel
from pydantic import Field

from model import Itinerary, Day
from park4night import getPlaces_park4Night
from secret_key import openapi_key

os.environ['OPENAI_API_KEY'] = openapi_key


def run_tools(input_message: AIMessage) -> list[BaseMessage]:
    messages = []
    if hasattr(input_message, 'tool_calls'):
        for tool_call in input_message.tool_calls:
            selected_tool = {"getPlaces_park4Night": getPlaces_park4Night}[tool_call["name"]]
            tool_msg = selected_tool.invoke(tool_call)
            messages.append(tool_msg)
    return messages


def generate_itinerary(destination: str, traveller_info: str) -> Itinerary:
    model: ChatOpenAI = ChatOpenAI()

    # First prompt
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", """You are a veteran tour guide.
            You help travellers organize individualized tours in their RV.
            When presented with a rough idea for the destination, you use your knowledge of interesting destination,
            tourist attractions as well as the locality to create a day-by-day itinerary.
            You take into account the needs of every traveller in order to come up with an individualized itinerary 
            personalized to the preferences of the traveller, be it a young women solo travelling in a converted car, 
            a family going on vacation in a camper van, or a retired couple going on extended RV trips.  
            """),
        ("user",
         """The destination for this trip is: {destination}. 
         The duration of this trip is 10 days. 
         The itinerary should cater towards the following type of traveller: '{traveller_info}'.
         
         Let's start by suggesting a city that acts as the start and end of the trip. It should be easy to reach, either
         for travellers flying in and renting a vehicle, or from travellers arriving in their own vehicle.
         Don't plan a fully itinerary yet. Return just the name of the place.""")
    ])

    messages = prompt_template.invoke({"destination": destination, "traveller_info": traveller_info}).messages

    class StartAndEndLocation(BaseModel):
        """A stop during a roadtrip"""
        location_name: str = Field(description="Name of the city, town to start and end the trip")

    start_and_end_location = model.with_structured_output(StartAndEndLocation).invoke(messages)
    messages.append(PromptTemplate.from_template(
        """Great! Let's use {start_and_end_location} as our starting place.
        Now, plan the next day. Where could we go from here?"""
    ).format(
        start_and_end_location=start_and_end_location.location_name
    ))
    
    ai_msg = model.bind_tools([getPlaces_park4Night]).invoke(messages)
    messages.append(ai_msg)

    # Resolve tools
    tool_messages = run_tools(ai_msg)
    messages.append(*tool_messages)

    # Get final answer
    response = model.with_structured_output(Day).invoke(messages)

    return response
