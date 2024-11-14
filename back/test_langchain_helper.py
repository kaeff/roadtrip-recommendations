from langchain_helper import generate_itinerary


def test_generate_roadtrip_stations():
    itinerary = generate_itinerary("France", "Mid 30s couple")
    print(itinerary)

    stations = itinerary.stops

    assert len(stations) > 0
    for station in stations:
        assert len(station.destination) > 0
        assert len(station.activities) > 0
        assert len(station.parking_options) > 0

