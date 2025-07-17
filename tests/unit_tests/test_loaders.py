from utilities import load_clubs, load_competitions, load_bookings


def test_loadClubs():
    clubs = [
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

    loaded_clubs = load_clubs()

    assert clubs == loaded_clubs


def test_loadCompetitions():

    competitions = [
        {
            "name": "Spring Festival",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "25"
        },
        {
            "name": "Fall Classic",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "13"
        },
        {
            "name": "Open Classic",
            "date": "2030-06-22 13:30:00",
            "numberOfPlaces": "11"
        },
        {
            "name": "Summer Games",
            "date": "2028-06-22 13:30:00",
            "numberOfPlaces": "32"
        }
    ]

    loaded_competitions = load_competitions()

    assert competitions == loaded_competitions


def test_loadBookings():
    bookings = []

    loaded_bookings = load_bookings()

    assert bookings == loaded_bookings
