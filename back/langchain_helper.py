import json
import os

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from secret_key import openapi_key

os.environ['OPENAI_API_KEY'] = openapi_key


class GeoCoordinates(BaseModel):
    latitude: float = Field()
    longitude: float = Field()


class ParkingPlace(BaseModel):
    name: str = Field()


class Day(BaseModel):
    """A stop during a roadtrip"""

    destination: str = Field(description="Name of a cities, town etc to visit during this day")
    activities: str = Field(description="Description of main activites or interests during this stop")
    coordinates: GeoCoordinates = Field(description="Geo coordinates (latitude, longitude) of the destination")
    parking_options: list[ParkingPlace] = Field(
        description="Parking for the night (Public parking suitable for large vehicles, campground, RV parking, nature spot etc")


class Itinerary(BaseModel):
    stops: list[Day] = Field()


@tool
def getPlaces_park4Night(latitude: float, longitude: float) -> str:
    """Returns a list of place names from park4night, a site for overnight parking spots for camper vans, RVs etc"""
    return json.dumps(["Sample parking A", "Sample parking B", "Sample parking C"])

def run_tools(input):
    messages = []
    if input.tool_calls:
        for tool_call in input.tool_calls:
            selected_tool = {"getPlaces_park4Night": getPlaces_park4Night}[tool_call["name"]]
            tool_msg = selected_tool.invoke(tool_call)
            messages.append(tool_msg)
    return messages

def make_chain():
    model: ChatOpenAI = ChatOpenAI()

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", """Schlage eine Route für eine Wohnmobiltour vor. 
        Schlage für jeden Tag einen Ort zum Stationieren vor, sowie interessante Aktivitäten am Ort oder entlang der Route.  
        Use park4night to find parking spots.
        """),
        ("user",
         """Das Ziel ist: {destination}. 
         Dauer: 10 Tage. 
         Die Route soll attraktiv sein für Reisende mit dem folgenden Profil: '{traveller_info}'.""")
    ])

    chain = (prompt_template |
             model.bind_tools([getPlaces_park4Night]) |
             RunnableLambda(run_tools) |
             model.with_structured_output(Itinerary)
             )
    return chain


chain = make_chain()


def generate_itinerary(destination: str, traveller_info: str) -> Itinerary:
    model: ChatOpenAI = ChatOpenAI()

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", """Schlage eine Route für eine Wohnmobiltour vor. 
            Schlage für jeden Tag einen Ort zum Stationieren vor, sowie interessante Aktivitäten am Ort oder entlang der Route.  
            Use park4night to find parking spots.
            """),
        ("user",
         """Das Ziel ist: {destination}. 
         Dauer: 10 Tage. 
         Die Route soll attraktiv sein für Reisende mit dem folgenden Profil: '{traveller_info}'.""")
    ])

    chat_prompt = prompt_template.invoke({"destination": destination, "traveller_info": traveller_info})
    ai_msg = model.bind_tools([getPlaces_park4Night]).invoke(chat_prompt)
    tool_msg = run_tools(ai_msg)
    messages = [*chat_prompt.to_messages(), ai_msg, *tool_msg]
    response = model.with_structured_output(Itinerary).invoke(messages)

    return response
