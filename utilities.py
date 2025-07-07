import json
from datetime import datetime


def load_clubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def load_competitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


def check_mail_exist(mail):
    clubs = load_clubs()
    for club in clubs:
        if club['email'] == mail:
            return True
    return False


def check_competion_is_open(date_competition):
    date_competition = datetime.strptime(date_competition, '%Y-%m-%d %H:%M:%S')
    if date_competition > datetime.today():
        return True
    return False
