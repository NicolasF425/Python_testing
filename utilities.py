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


def load_bookings():
    with open('bookings.json') as books:
        listOfBookings = json.load(books)['bookings']
        return listOfBookings


def check_booking_exist(club_name, competition_name, bookings):
    if bookings != []:
        for booking in bookings:
            if club_name == booking['club'] and competition_name == booking['competition']:
                return True
    return False


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
