import os

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from secret_key import openapi_key

os.environ['OPENAI_API_KEY'] = openapi_key


class GeoCoordinates(BaseModel):
    latitude: float = Field()
    longitude: float = Field()

class Day(BaseModel):
    """A stop during a roadtrip"""

    destination: str = Field(description="Name of a cities, town etc to visit during this day")
    activities: str = Field(description="Description of main activites or interests during this stop")
    coordinates: GeoCoordinates = Field(description="Geo coordinates (latitude, longitude) of the destination")

class Itinerary(BaseModel):
    stops: list[Day] = Field()

def make_chain():
    model = ChatOpenAI()
    structured_model = model.with_structured_output(Itinerary)
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", """Schlage eine Route für eine Wohnmobiltour vor. 
        Schlage für jeden Tag einen Ort zum Stationieren vor, sowie interessante Aktivitäten am Ort oder entlang der Route.  
        """),
        ("user",
         """Das Ziel ist: {destination}. 
         Dauer: 10 Tage. 
         Die Route soll attraktiv sein für Reisende mit dem folgenden Profil: '{traveller_info}'.""")
    ])
    chain = prompt_template | structured_model
    return chain

chain = make_chain()

def generate_itinerary(destination: str, traveller_info: str) -> Itinerary:
    response = chain.invoke({
        'destination': destination,
        'traveller_info': traveller_info
    })

    return response