# locustfile.py - Fichier principal des tests de performance
from locust import HttpUser, task, between, SequentialTaskSet
import random
import json
from datetime import datetime, timedelta

class WebsiteUser(HttpUser):
    """Utilisateur simulé pour les tests de performance"""
    
    # Temps d'attente entre les requêtes (en secondes)
    wait_time = between(1, 5)
    
    # Données de test
    test_clubs = [
        {"name": "Simply Lift", "email": "john@simplylift.co", "points": 13},
        {"name": "Iron Temple", "email": "admin@irontemple.com", "points": 4},
        {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": 12}
    ]
    
    test_competitions = [
        {"name": "Spring Festival", "numberOfPlaces": 25},
        {"name": "Fall Classic", "numberOfPlaces": 13}
    ]
    
    def on_start(self):
        """Méthode appelée au démarrage de chaque utilisateur"""
        self.client.verify = False  # Désactive la vérification SSL si nécessaire
        self.selected_club = random.choice(self.test_clubs)
        print(f"Utilisateur démarré avec le club: {self.selected_club['name']}")
    
    @task(3)
    def view_homepage(self):
        """Test de charge de la page d'accueil"""
        with self.client.get("/", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Page d'accueil non accessible: {response.status_code}")
    
    @task(5)
    def login_process(self):
        """Test du processus de connexion"""
        # Accès à la page d'accueil
        self.client.get("/")
        
        # Tentative de connexion
        with self.client.post("/showSummary", 
                            data={"email": self.selected_club["email"]},
                            catch_response=True) as response:
            if response.status_code == 200 and b"Welcome" in response.content:
                response.success()
            else:
                response.failure(f"Échec de connexion: {response.status_code}")
    
    @task(2)
    def view_clubs_points(self):
        """Test de la page d'affichage des points"""
        with self.client.get("/points", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Page des points non accessible: {response.status_code}")
    
    @task(1)
    def booking_flow(self):
        """Test du flux de réservation complet"""
        # Connexion
        self.client.post("/showSummary", data={"email": self.selected_club["email"]})
        
        # Accès à la page de réservation
        competition = random.choice(self.test_competitions)
        booking_url = f"/book/{competition['name']}/{self.selected_club['name']}"
        
        with self.client.get(booking_url, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Page de réservation non accessible: {response.status_code}")
        
        # Tentative d'achat de places
        places_to_book = random.randint(1, min(5, self.selected_club["points"]))
        with self.client.post("/purchasePlaces", 
                            data={
                                "competition": competition["name"],
                                "club": self.selected_club["name"],
                                "places": str(places_to_book)
                            },
                            catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Échec de l'achat: {response.status_code}")

class SequentialUserBehavior(SequentialTaskSet):
    """Comportement séquentiel d'un utilisateur"""
    
    def on_start(self):
        self.club = random.choice([
            {"name": "Simply Lift", "email": "john@simplylift.co"},
            {"name": "Iron Temple", "email": "admin@irontemple.com"},
            {"name": "She Lifts", "email": "kate@shelifts.co.uk"}
        ])
    
    @task
    def step1_visit_homepage(self):
        """Étape 1: Visite de la page d'accueil"""
        self.client.get("/")
    
    @task
    def step2_login(self):
        """Étape 2: Connexion"""
        self.client.post("/showSummary", data={"email": self.club["email"]})
    
    @task
    def step3_view_points(self):
        """Étape 3: Consultation des points"""
        self.client.get("/points")
    
    @task
    def step4_book_competition(self):
        """Étape 4: Réservation d'une compétition"""
        self.client.get("/book/Spring Festival/Simply Lift")
    
    @task
    def step5_purchase(self):
        """Étape 5: Achat de places"""
        self.client.post("/purchasePlaces", data={
            "competition": "Spring Festival",
            "club": self.club["name"],
            "places": "2"
        })
    
    @task
    def step6_logout(self):
        """Étape 6: Déconnexion"""
        self.client.get("/logout")

class SequentialUser(HttpUser):
    """Utilisateur avec comportement séquentiel"""
    tasks = [SequentialUserBehavior]
    wait_time = between(1, 3)

# Tests de performance spécifiques
class StressTestUser(HttpUser):
    """Utilisateur pour tests de stress"""
    wait_time = between(0.1, 0.5)  # Temps d'attente réduit pour plus de stress
    
    @task(10)
    def rapid_homepage_access(self):
        """Accès rapide à la page d'accueil"""
        self.client.get("/")
    
    @task(5)
    def rapid_login_attempts(self):
        """Tentatives de connexion rapides"""
        emails = ["john@simplylift.co", "admin@irontemple.com", "kate@shelifts.co.uk"]
        email = random.choice(emails)
        self.client.post("/showSummary", data={"email": email})
    
    @task(3)
    def rapid_points_view(self):
        """Consultation rapide des points"""
        self.client.get("/points")

class LoadTestUser(HttpUser):
    """Utilisateur pour tests de charge prolongée"""
    wait_time = between(2, 8)
    
    @task(4)
    def normal_navigation(self):
        """Navigation normale"""
        self.client.get("/")
        self.client.get("/points")
    
    @task(2)
    def login_and_browse(self):
        """Connexion et navigation"""
        self.client.post("/showSummary", data={"email": "john@simplylift.co"})
        self.client.get("/book/Spring Festival/Simply Lift")

# Configuration personnalisée pour différents scénarios
class CustomLoadTest(HttpUser):
    """Test de charge personnalisé avec métriques"""
    wait_time = between(1, 4)
    
    def on_start(self):
        """Initialisation avec métriques personnalisées"""
        self.start_time = datetime.now()
    
    @task
    def timed_login_flow(self):
        """Flux de connexion avec mesure du temps"""
        start = datetime.now()
        
        # Page d'accueil
        response1 = self.client.get("/")
        
        # Connexion
        response2 = self.client.post("/showSummary", 
                                   data={"email": "john@simplylift.co"})
        
        # Calcul du temps total
        total_time = (datetime.now() - start).total_seconds()
        
        # Log des performances
        if total_time > 2.0:  # Plus de 2 secondes
            print(f"Flux de connexion lent: {total_time:.2f}s")
        
        # Vérification des réponses
        if response1.status_code != 200 or response2.status_code != 200:
            print(f"Erreur dans le flux: {response1.status_code}, {response2.status_code}")

# Configuration pour différents environnements
class ProductionLikeUser(HttpUser):
    """Utilisateur simulant un environnement de production"""
    wait_time = between(5, 15)  # Temps d'attente plus réaliste
    
    # Poids des tâches basés sur l'usage réel
    @task(20)
    def browse_homepage(self):
        """Navigation sur la page d'accueil (usage le plus fréquent)"""
        self.client.get("/")
    
    @task(10)
    def check_points(self):
        """Consultation des points"""
        self.client.get("/points")
    
    @task(5)
    def login_process(self):
        """Processus de connexion"""
        emails = ["john@simplylift.co", "admin@irontemple.com", "kate@shelifts.co.uk"]
        email = random.choice(emails)
        self.client.post("/showSummary", data={"email": email})
    
    @task(2)
    def booking_process(self):
        """Processus de réservation (moins fréquent mais plus critique)"""
        self.client.post("/showSummary", data={"email": "john@simplylift.co"})
        self.client.get("/book/Spring Festival/Simply Lift")
        self.client.post("/purchasePlaces", data={
            "competition": "Spring Festival",
            "club": "Simply Lift",
            "places": "3"
        })

# Fichier de configuration (locust.conf)
"""
# locust.conf - Configuration pour Locust
[locust]
locustfile = locustfile.py
host = http://localhost:5000
users = 50
spawn-rate = 5
run-time = 5m
html = report.html
csv = results
loglevel = INFO
"""

# Scripts de lancement pour différents scénarios

# run_basic_test.py - Script pour test de base
"""
#!/usr/bin/env python3
import subprocess
import sys

def run_basic_test():
    cmd = [
        'locust',
        '-f', 'locustfile.py',
        '--host', 'http://localhost:5000',
        '--users', '10',
        '--spawn-rate', '2',
        '--run-time', '2m',
        '--html', 'basic_test_report.html',
        '--headless'
    ]
    
    print("Démarrage du test de base...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("Test de base terminé avec succès!")
        print(f"Rapport généré: basic_test_report.html")
    else:
        print(f"Erreur lors du test: {result.stderr}")
        sys.exit(1)

if __name__ == "__main__":
    run_basic_test()
"""

# run_stress_test.py - Script pour test de stress
"""
#!/usr/bin/env python3
import subprocess

def run_stress_test():
    cmd = [
        'locust',
        '-f', 'locustfile.py',
        '--host', 'http://localhost:5000',
        '--users', '100',
        '--spawn-rate', '10',
        '--run-time', '10m',
        '--html', 'stress_test_report.html',
        '--csv', 'stress_test_results',
        '--headless'
    ]
    
    print("Démarrage du test de stress...")
    subprocess.run(cmd)

if __name__ == "__main__":
    run_stress_test()
"""

# Commandes pour exécuter les tests :
"""
# Installation
pip install locust

# Test de base avec interface web
locust -f locustfile.py --host http://localhost:5000

# Test automatisé (headless)
locust -f locustfile.py --host http://localhost:5000 --users 50 --spawn-rate 5 --run-time 2m --html report.html --headless

# Test de stress
locust -f locustfile.py --host http://localhost:5000 --users 100 --spawn-rate 10 --run-time 10m --html stress_report.html --headless

# Test avec utilisateur séquentiel
locust -f locustfile.py --host http://localhost:5000 --users 20 --spawn-rate 2 --run-time 5m --html sequential_report.html --headless SequentialUser

# Test spécifique de stress
locust -f locustfile.py --host http://localhost:5000 --users 200 --spawn-rate 20 --run-time 15m --html stress_report.html --headless StressTestUser
"""
