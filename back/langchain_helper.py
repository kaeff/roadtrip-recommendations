import os

from langchain_core.messages import AIMessage, BaseMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from model import Itinerary
from park4night import getPlaces_park4Night
from secret_key import openapi_key

os.environ['OPENAI_API_KEY'] = openapi_key


def run_tools(input_message: AIMessage) -> list[BaseMessage]:
    messages = []
    if input_message.tool_calls:
        for tool_call in input_message.tool_calls:
            selected_tool = {"getPlaces_park4Night": getPlaces_park4Night}[tool_call["name"]]
            tool_msg = selected_tool.invoke(tool_call)
            messages.append(tool_msg)
    return messages

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
