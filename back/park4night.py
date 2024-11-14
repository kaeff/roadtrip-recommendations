import requests
from langchain_core.tools import tool
from pydantic_core import ValidationError

from model import ParkingPlace


@tool
def getPlaces_park4Night(latitude: float, longitude: float) -> list[ParkingPlace]:
    """Returns a list of place names from park4night, a site for overnight parking spots for camper vans, RVs etc"""

    places = []
    url = f"https://guest.park4night.com/services/V4.1/lieuxGetFilter.php?latitude={latitude}&longitude={longitude}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        places_json = [place for place in data.get("lieux", []) if place["code"] in _suitable_place_codes]
        places_json = sorted(places_json, key=lambda x: float(x["note_moyenne"] or "-1"), reverse=True)[:10]

        try:
            places = [
                ParkingPlace.model_validate({
                    "name": place["titre"],
                    "coordinates": {"latitude": place["latitude"], "longitude": place["longitude"]},
                    "code": place["code"],
                    "rating_average": place["note_moyenne"]
                })
                for place in places_json
            ]
        except ValidationError as e:
            print(e)

    return places


_suitable_place_codes = ["APN", "ASS", "C", "P", "PN", "ACC_P", "ACC_G", "ACC_PR", "PSS", "F", "EP"]
