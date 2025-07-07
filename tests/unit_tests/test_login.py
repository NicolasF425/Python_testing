import pytest
from server import app


@pytest.fixture
def client():
    """Fixture pour créer un client de test Flask"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_login_KO(client):
    rv = client.post("/showSummary", data={
        'email': 'toto@false.com'
    }, follow_redirects=True)

    assert rv.status_code == 200
    data = rv.data.decode()

    assert "Mail unknown, please retry" in data


def test_login_OK(client):
    rv = client.post("/showSummary", data={
        'email': 'john@simplylift.co'
    }, follow_redirects=True)

    assert rv.status_code == 200
    data = rv.data.decode()

    assert "Welcome" in data
