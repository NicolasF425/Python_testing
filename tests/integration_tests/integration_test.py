import pytest
from server import app, clubs, competitions


@pytest.fixture
def client():
    """Fixture pour créer un client de test Flask"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_integration(client):

    placesToReserve = 3

    rv = client.post("/showSummary", data={
        'email': clubs[0]['email']
    }, follow_redirects=True)

    assert rv.status_code == 200
    data = rv.data.decode()
    assert "Welcome" in data

    competition_name = competitions[2]['name']
    club_name = clubs[0]['name']

    # Sauvegarde des valeurs initiales
    initial_points = int(clubs[0]['points'])
    initial_places = int(competitions[2]['numberOfPlaces'])

    rv = client.get(f"/book/{competition_name}/{club_name}")
    assert rv.status_code == 200

    rv = client.post("/purchasePlaces", data={"competition": competition_name,
                                              "club": club_name, 'places': placesToReserve})

    assert rv.status_code == 200
    data = rv.data.decode()

    assert "Great-booking complete!" in data

    # Vérificaion des modifications
    updated_club = [c for c in clubs if c['name'] == club_name][0]
    updated_competition = [c for c in competitions if c['name'] == competition_name][0]

    assert int(updated_club['points']) == initial_points - placesToReserve
    assert int(updated_competition['numberOfPlaces']) == initial_places - placesToReserve
