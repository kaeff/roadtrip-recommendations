from langchain_helper import generate_roadtrip_stations, transform_response


def test_generate_roadtrip_stations():
    stations = generate_roadtrip_stations("France", "Mid 30s couple")
    print(stations)
    assert len(stations) > 0
    for station in stations:
        assert len(station.place) > 0
        assert len(station.description) > 0


def test_transform_response():
    response = {
        "destination": "France",
        "traveller_info": "Mid 30s couple",
        "trip_stations": "\nParis, Frankreich; Besichtigung des Eiffelturms, Spaziergang entlang der Seine, Besuch des Louvre Museums\nVersailles, Frankreich; Besichtigung des Schlosses von Versailles, Picknick im Schlossgarten\nLyon, Frankreich; Besuch der Basilika Notre-Dame de Fourvi\u00e8re, Spaziergang durch die Altstadt, Verkostung von Lyoner Spezialit\u00e4ten\nAvignon, Frankreich; Besuch des Papstpalastes, Spaziergang \u00fcber die Pont d'Avignon, Weinprobe in der Region Ch\u00e2teauneuf-du-Pape\nCarcassonne, Frankreich; Besichtigung der mittelalterlichen Stadtmauer, Besuch des Schlosses Comtal, Kanufahrt auf dem Canal du Midi\nBiarritz, Frankreich; Entspannen am Strand, Surfen in der Bucht von Biscaya, Besuch des Aquariums\nBordeaux, Frankreich; Besichtigung des Place de la Bourse, Weinprobe in der Region Saint-\u00c9milion, Spaziergang durch die Altstadt\nLa Rochelle, Frankreich; Besuch des H"
    }

    result = transform_response(response)

    assert result[0].place == "Paris, Frankreich"
    assert result[0].description == "Besichtigung des Eiffelturms, Spaziergang entlang der Seine, Besuch des Louvre Museums"

