# tests/conftest.py - Configuration des fixtures pytest
import pytest
import tempfile
import json
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
from app import app

@pytest.fixture
def client():
    """Fixture pour le client de test Flask"""
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.test_client() as client:
        with app.app_context():
            yield client

@pytest.fixture
def mock_clubs():
    """Fixture pour les données de clubs de test"""
    return [
        {
            "name": "Simply Lift",
            "email": "john@simplylift.co",
            "points": "13"
        },
        {
            "name": "Iron Temple",
            "email": "admin@irontemple.com",
            "points": "4"
        },
        {
            "name": "She Lifts",
            "email": "kate@shelifts.co.uk",
            "points": "12"
        }
    ]

@pytest.fixture
def mock_competitions():
    """Fixture pour les données de compétitions de test"""
    future_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')
    past_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')
    
    return [
        {
            "name": "Spring Festival",
            "date": future_date,
            "numberOfPlaces": "25"
        },
        {
            "name": "Fall Classic",
            "date": future_date,
            "numberOfPlaces": "13"
        },
        {
            "name": "Past Competition",
            "date": past_date,
            "numberOfPlaces": "10"
        }
    ]

@pytest.fixture
def mock_utilities():
    """Fixture pour mocker les fonctions utilitaires"""
    with patch('app.loadClubs') as mock_load_clubs, \
         patch('app.loadCompetitions') as mock_load_competitions, \
         patch('app.checkMailExist') as mock_check_mail, \
         patch('app.checkCompetionIsOpen') as mock_check_competition_open:
        
        yield {
            'loadClubs': mock_load_clubs,
            'loadCompetitions': mock_load_competitions,
            'checkMailExist': mock_check_mail,
            'checkCompetionIsOpen': mock_check_competition_open
        }

# tests/test_integration.py - Tests d'intégration
import pytest
from unittest.mock import patch
from datetime import datetime, timedelta

class TestFlaskIntegration:
    """Tests d'intégration pour l'application Flask GUDLFT"""
    
    def test_index_page_loads(self, client):
        """Test que la page d'accueil se charge correctement"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Welcome to the GUDLFT Registration Portal!' in response.data or b'index' in response.data
    
    @patch('app.clubs')
    @patch('app.competitions')
    @patch('app.checkMailExist')
    def test_show_summary_valid_email(self, mock_check_mail, mock_competitions, mock_clubs, client, mock_clubs, mock_competitions):
        """Test connexion avec email valide"""
        # Configuration des mocks
        mock_clubs.return_value = mock_clubs
        mock_competitions.return_value = mock_competitions
        mock_check_mail.return_value = True
        
        # Patcher les variables globales
        with patch('app.clubs', mock_clubs), \
             patch('app.competitions', mock_competitions):
            
            response = client.post('/showSummary', data={
                'email': 'john@simplylift.co'
            })
            
            assert response.status_code == 200
            assert b'Welcome' in response.data or b'Points available' in response.data
    
    @patch('app.checkMailExist')
    def test_show_summary_invalid_email(self, mock_check_mail, client):
        """Test connexion avec email invalide"""
        mock_check_mail.return_value = False
        
        response = client.post('/showSummary', data={
            'email': 'invalid@email.com'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Mail unknown, please retry' in response.data
    
    @patch('app.clubs')
    @patch('app.competitions')
    def test_book_valid_competition_and_club(self, mock_competitions, mock_clubs, client, mock_clubs, mock_competitions):
        """Test réservation avec compétition et club valides"""
        with patch('app.clubs', mock_clubs), \
             patch('app.competitions', mock_competitions):
            
            response = client.get('/book/Spring Festival/Simply Lift')
            assert response.status_code == 200
            assert b'booking' in response.data.lower() or b'places' in response.data.lower()
    
    @patch('app.clubs')
    @patch('app.competitions')
    def test_book_invalid_competition_or_club(self, mock_competitions, mock_clubs, client, mock_clubs, mock_competitions):
        """Test réservation avec compétition ou club invalides"""
        with patch('app.clubs', mock_clubs), \
             patch('app.competitions', mock_competitions):
            
            response = client.get('/book/Invalid Competition/Simply Lift')
            assert response.status_code == 200
            assert b'Something went wrong' in response.data
    
    @patch('app.clubs')
    @patch('app.competitions') 
    @patch('app.checkCompetionIsOpen')
    def test_purchase_places_success(self, mock_check_open, mock_competitions, mock_clubs, client, mock_clubs, mock_competitions):
        """Test achat de places avec succès"""
        mock_check_open.return_value = True
        
        with patch('app.clubs', mock_clubs), \
             patch('app.competitions', mock_competitions):
            
            response = client.post('/purchasePlaces', data={
                'competition': 'Spring Festival',
                'club': 'Simply Lift',
                'places': '5'
            })
            
            assert response.status_code == 200
            assert b'Great-booking complete!' in response.data
    
    @patch('app.clubs')
    @patch('app.competitions')
    @patch('app.checkCompetionIsOpen')
    def test_purchase_places_not_enough_points(self, mock_check_open, mock_competitions, mock_clubs, client, mock_clubs, mock_competitions):
        """Test achat de places sans assez de points"""
        mock_check_open.return_value = True
        
        with patch('app.clubs', mock_clubs), \
             patch('app.competitions', mock_competitions):
            
            response = client.post('/purchasePlaces', data={
                'competition': 'Spring Festival',
                'club': 'Iron Temple',  # Club avec seulement 4 points
                'places': '10'  # Demande 10 places
            })
            
            assert response.status_code == 200
            assert b'Not enough points !' in response.data
    
    @patch('app.clubs')
    @patch('app.competitions')
    @patch('app.checkCompetionIsOpen')
    def test_purchase_places_too_many_places(self, mock_check_open, mock_competitions, mock_clubs, client, mock_clubs, mock_competitions):
        """Test achat de plus de 12 places"""
        mock_check_open.return_value = True
        
        with patch('app.clubs', mock_clubs), \
             patch('app.competitions', mock_competitions):
            
            response = client.post('/purchasePlaces', data={
                'competition': 'Spring Festival',
                'club': 'Simply Lift',
                'places': '15'  # Plus de 12 places
            })
            
            assert response.status_code == 200
            assert b'12 places maximum !' in response.data
    
    @patch('app.clubs')
    @patch('app.competitions')
    @patch('app.checkCompetionIsOpen')
    def test_purchase_places_not_enough_available(self, mock_check_open, mock_competitions, mock_clubs, client, mock_clubs, mock_competitions):
        """Test achat de places quand pas assez disponibles"""
        mock_check_open.return_value = True
        
        with patch('app.clubs', mock_clubs), \
             patch('app.competitions', mock_competitions):
            
            response = client.post('/purchasePlaces', data={
                'competition': 'Fall Classic',  # Seulement 13 places disponibles
                'club': 'Simply Lift',
                'places': '15'  # Demande 15 places
            })
            
            assert response.status_code == 200
            assert b'You cant reserve that much places !' in response.data
    
    @patch('app.clubs')
    @patch('app.competitions')
    @patch('app.checkCompetionIsOpen')
    def test_purchase_places_competition_closed(self, mock_check_open, mock_competitions, mock_clubs, client, mock_clubs, mock_competitions):
        """Test achat de places pour compétition fermée"""
        mock_check_open.return_value = False
        
        with patch('app.clubs', mock_clubs), \
             patch('app.competitions', mock_competitions):
            
            response = client.post('/purchasePlaces', data={
                'competition': 'Past Competition',
                'club': 'Simply Lift',
                'places': '5'
            })
            
            assert response.status_code == 200
            assert b'Competition closed !' in response.data
    
    @patch('app.clubs')
    def test_display_clubs_points(self, mock_clubs, client, mock_clubs):
        """Test affichage des points des clubs"""
        with patch('app.clubs', mock_clubs):
            response = client.get('/points')
            assert response.status_code == 200
            assert b'Simply Lift' in response.data
            assert b'Iron Temple' in response.data
            assert b'She Lifts' in response.data
    
    def test_logout_redirects_to_index(self, client):
        """Test que logout redirige vers l'index"""
        response = client.get('/logout')
        assert response.status_code == 302
        assert '/logout' not in response.location
    
    def test_logout_redirect_followed(self, client):
        """Test que logout redirige effectivement vers l'index"""
        response = client.get('/logout', follow_redirects=True)
        assert response.status_code == 200

class TestWorkflowIntegration:
    """Tests d'intégration pour les workflows complets"""
    
    @patch('app.clubs')
    @patch('app.competitions')
    @patch('app.checkMailExist')
    @patch('app.checkCompetionIsOpen')
    def test_complete_booking_workflow(self, mock_check_open, mock_check_mail, mock_competitions, mock_clubs, client, mock_clubs, mock_competitions):
        """Test du workflow complet de réservation"""
        # Configuration des mocks
        mock_check_mail.return_value = True
        mock_check_open.return_value = True
        
        with patch('app.clubs', mock_clubs), \
             patch('app.competitions', mock_competitions):
            
            # 1. Connexion avec email
            response = client.post('/showSummary', data={
                'email': 'john@simplylift.co'
            })
            assert response.status_code == 200
            
            # 2. Accès à la page de réservation
            response = client.get('/book/Spring Festival/Simply Lift')
            assert response.status_code == 200
            
            # 3. Achat de places
            response = client.post('/purchasePlaces', data={
                'competition': 'Spring Festival',
                'club': 'Simply Lift',
                'places': '5'
            })
            assert response.status_code == 200
            assert b'Great-booking complete!' in response.data
    
    @patch('app.clubs')
    @patch('app.competitions')
    @patch('app.checkMailExist')
    @patch('app.checkCompetionIsOpen')
    def test_multiple_bookings_same_session(self, mock_check_open, mock_check_mail, mock_competitions, mock_clubs, client, mock_clubs, mock_competitions):
        """Test plusieurs réservations dans la même session"""
        mock_check_mail.return_value = True
        mock_check_open.return_value = True
        
        with patch('app.clubs', mock_clubs), \
             patch('app.competitions', mock_competitions):
            
            # Première réservation
            client.post('/showSummary', data={'email': 'john@simplylift.co'})
            client.post('/purchasePlaces', data={
                'competition': 'Spring Festival',
                'club': 'Simply Lift',
                'places': '3'
            })
            
            # Deuxième réservation
            response = client.post('/purchasePlaces', data={
                'competition': 'Fall Classic',
                'club': 'Simply Lift',
                'places': '5'
            })

            assert response.status_code == 200
            # Vérifier que les points ont été correctement déduits
            # (Dans un vrai test, on vérifierait l'état des données)


# tests/test_edge_cases.py - Tests de cas limites
class TestEdgeCases:
    """Tests pour les cas limites et d'erreur"""
    
    def test_empty_form_submission(self, client):
        """Test soumission de formulaire vide"""
        response = client.post('/showSummary', data={})
        assert response.status_code in [400, 500]  # Erreur attendue
    
    def test_invalid_route(self, client):
        """Test accès à une route invalide"""
        response = client.get('/invalid-route')
        assert response.status_code == 404
    
    @patch('app.clubs')
    @patch('app.competitions')
    def test_book_with_special_characters(self, mock_competitions, mock_clubs, client):
        """Test réservation avec caractères spéciaux"""
        with patch('app.clubs', []), \
             patch('app.competitions', []):
            
            response = client.get('/book/Competition%20Name/Club%20Name')
            assert response.status_code == 200
    
    @patch('app.clubs')
    @patch('app.competitions')
    @patch('app.checkCompetionIsOpen')
    def test_purchase_zero_places(self, mock_check_open, mock_competitions, mock_clubs, client, mock_clubs, mock_competitions):
        """Test achat de 0 places"""
        mock_check_open.return_value = True
        
        with patch('app.clubs', mock_clubs), \
             patch('app.competitions', mock_competitions):
            
            response = client.post('/purchasePlaces', data={
                'competition': 'Spring Festival',
                'club': 'Simply Lift',
                'places': '0'
            })
            
            assert response.status_code == 200
            # Devrait soit accepter soit rejeter - selon la logique métier

# Commandes pour exécuter les tests :
# pip install pytest flask
# pytest tests/test_integration.py -v
# pytest tests/test_integration.py::TestFlaskIntegration::test_purchase_places_success -v
# pytest tests/ -v --tb=short