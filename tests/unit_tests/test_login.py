import pytest
from server import app


@pytest.fixture
def client():
    """Fixture pour créer un client de test Flask"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_login(client):
    rv = client.post("/", data={
        'email': 'john@simplylift.co'
    }, follow_redirects=True)

    assert rv.status_code == 200
    data = rv.data.decode()

    assert "Welcome" in data
