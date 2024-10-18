from langchain_helper import generate_roadtrip_stations


def test_generate_roadtrip_stations():
    stations = generate_roadtrip_stations("France", "Mid 30s couple")
    print(stations)
    assert len(stations) > 0
    for station in stations:
        assert len(station.place) > 0
