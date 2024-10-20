import json
import os
from collections import namedtuple

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import OpenAI, ChatOpenAI

from secret_key import openapi_key

os.environ['OPENAI_API_KEY'] = openapi_key

model = ChatOpenAI()

Stop = namedtuple('Stop', ['place', 'description'])


def generate_roadtrip_stations(destination: str, traveller_info: str) -> list[Stop]:
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
    parser = StrOutputParser()

    chain = prompt_template | model | parser

    response = chain.invoke({
        'destination': destination,
        'traveller_info': traveller_info
    })

    print(json.dumps(response, indent=4))

    stops_objects = transform_response(response)

    return stops_objects


def transform_response(response):
    stops_csv = [s.split(";") for s in response.split('\n')]
    stops_csv = [line[0:2] for line in stops_csv if len(line) > 0 and len(line[0]) > 0]
    stops_csv = [[cell.strip() for cell in line] for line in stops_csv]
    stops_objects = [Stop._make(line) for line in stops_csv]
    return stops_objects
