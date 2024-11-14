from enum import Enum

from pydantic import BaseModel, Field


class GeoCoordinates(BaseModel):
    latitude: float = Field()
    longitude: float = Field()


class ParkingPlaceCode(str, Enum):
    picnick_area = "APN"
    service_area = "ASS"
    camping = "C"
    services = "DS"
    offroad = "OR"
    parking_day_and_night = "P"
    parking_daytime = "PJ"
    surrounded_by_nature = "PN"
    motorhome_area_paid = "ACC_P"
    motorhome_area_free = "ACC_G"
    motorhome_area_private = "ACC_PR"
    motorhome_parking_without_service = "PSS"
    farmstay = "F"
    homestay_accomodation = "EP"


class ParkingPlace(BaseModel):
    name: str = Field()
    coordinates: GeoCoordinates = Field()
    code: ParkingPlaceCode = Field()
    rating_average: str = Field()

class Day(BaseModel):
    """A stop during a roadtrip"""

    destination: str = Field(description="Name of a cities, town etc to visit during this day")
    activities: str = Field(description="Description of main activites or interests during this stop")
    coordinates: GeoCoordinates = Field(description="Geo coordinates (latitude, longitude) of the destination")
    parking_options: list[ParkingPlace] = Field(
        description="Parking for the night (Public parking suitable for large vehicles, campground, RV parking, nature spot etc")


class Itinerary(BaseModel):
    stops: list[Day] = Field()
