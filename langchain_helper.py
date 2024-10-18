import json
import os
from collections import namedtuple
from typing import Dict, Any, List

from langchain.chains.llm import LLMChain
from langchain.chains.sequential import SequentialChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI

from secret_key import openapi_key

os.environ['OPENAI_API_KEY'] = openapi_key

llm = OpenAI(model_name="gpt-3.5-turbo-instruct", temperature=0.6)

Stop = namedtuple('Stop', ['place', 'description'])

def generate_roadtrip_stations(destination: str, traveller_info: str) -> list[Stop]:
    prompt_template = PromptTemplate(
        input_variables=['destination', 'traveller_info'],
        template=f"""Schlage eine Route für eine Wohnmobiltour vor. 
        Das Ziel ist: {destination}. Dauer: 10 Tage. 
        Die Route soll attraktiv sein für Reisende mit dem folgenden Profil: '{traveller_info}'. 
        Entferne die Anreise; der Startpunkt ist der erste Halt in der Zielregion. 
        Schlage für jeden Tag einen Ort zum Stationieren vor, sowie interessante Aktivitäten am Ort.  
        Eine Zeile pro Tag, Format: '<Ort>, <Land>;<Aktivitäten>'. Keine Nummerierung wie "Tag 1" etc
        """
    )

    stations_chain = LLMChain(llm=llm,
                              prompt=prompt_template,
                              output_key='trip_stations')

    chain = SequentialChain(
        chains=[stations_chain],
        input_variables=['destination', 'traveller_info'],
        output_variables=['trip_stations']
    )

    response = chain({'destination': destination,
                      'traveller_info': traveller_info
                      })

    print(json.dumps(response, indent=4))

    stops_objects = transform_response(response)

    return stops_objects


def transform_response(response):
    stops_csv = [s.split(";") for s in response['trip_stations'].split('\n')]
    stops_csv = [line[0:2] for line in stops_csv if len(line) > 0 and len(line[0]) > 0]
    stops_csv = [[cell.strip() for cell in line] for line in stops_csv]
    stops_objects = [Stop._make(line) for line in stops_csv]
    return stops_objects