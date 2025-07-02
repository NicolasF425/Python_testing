import pytest
from server import app


@pytest.fixture
def client():
    """Fixture pour créer un client de test Flask"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_purchasePlaces_success(client):
    rv = client.post("/purchasePlaces", data={
        'club': 'Simply Lift',
        'competition': 'Open Classic',
        'places': '3'
    }, follow_redirects=True)

    assert rv.status_code == 200
    data = rv.data.decode()

    assert "Great-booking complete!" in data


def test_purchasePlaces_tooLate(client):
    rv = client.post("/purchasePlaces", data={
        'club': 'Simply Lift',
        'competition': 'Spring Festival',
        'places': '3'
    }, follow_redirects=True)

    assert rv.status_code == 200
    data = rv.data.decode()

    assert "Competition closed !" in data
