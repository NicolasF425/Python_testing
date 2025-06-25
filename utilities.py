import json


def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


def checkMailExist(mail):
    clubs = loadClubs()
    for club in clubs:
        if club['email'] == mail:
            return True
    return False
