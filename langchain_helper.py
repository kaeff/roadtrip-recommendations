import os

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from secret_key import openapi_key

os.environ['OPENAI_API_KEY'] = openapi_key


class Stop(BaseModel):
    place: str = Field(description="Name of a city, town etc to stop during a roadtrip")
    description: str = Field(description="Short rationale of main activites or interests during this stop")

class Itinerary(BaseModel):
    stops: list[Stop] = Field()

model = ChatOpenAI()
structured_model = model.with_structured_output(Itinerary)

def generate_itinerary(destination: str, traveller_info: str) -> Itinerary:
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", """Schlage eine Route für eine Wohnmobiltour vor. 
        Entferne die Anreise; der Startpunkt ist der erste Halt in der Zielregion. 
        Schlage für jeden Tag einen Ort zum Stationieren vor, sowie interessante Aktivitäten am Ort.  
        Eine Zeile pro Tag, Format: '<Ort>, <Land>;<Aktivitäten>'. Keine Nummerierung wie "Tag 1" etc
        """),
        ("user",
         """Das Ziel ist: {destination}. 
         Dauer: 10 Tage. 
         Die Route soll attraktiv sein für Reisende mit dem folgenden Profil: '{traveller_info}'.""")
    ])
    chain = prompt_template | structured_model

    response = chain.invoke({
        'destination': destination,
        'traveller_info': traveller_info
    })

    return response