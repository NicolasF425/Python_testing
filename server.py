from flask import Flask, render_template, request, redirect, flash, url_for
from utilities import load_clubs, load_competitions, load_bookings
from utilities import check_booking_exist, check_mail_exist, check_competion_is_open


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = load_competitions()
clubs = load_clubs()
bookings = load_bookings()


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def showSummary():
    if check_mail_exist(request.form['email']):
        club = [club for club in clubs if club['email'] == request.form['email']][0]

        # Ajout de la vérification de date pour chaque compétition
        for comp in competitions:
            try:
                comp['is_future'] = check_competion_is_open(comp['date'])
            except ValueError:
                # En cas d'erreur, considérer comme future par sécurité
                comp['is_future'] = True

        return render_template('welcome.html', club=club, competitions=competitions)
    else:
        flash("Mail unknown, please retry")
        return redirect(url_for('index'))


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub == [] or foundCompetition == []:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)
    else:
        # Checking if the club has already reserved for the competition
        booking_exist = check_booking_exist(club, competition, bookings)
        # If exists retreiving datas
        if booking_exist:
            booking = [b for b in bookings if b['club'] == club
                       and b['competition'] == competition][0]
            max_places = 12-int(booking['places'])
        else:
            max_places = "12"
        return render_template('booking.html', club=foundClub, competition=foundCompetition, max_places=max_places)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    points_ok = True
    max_places_ok = True
    enough_places = True

    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]

    # Checking if the club has already reserved for the competition
    booking_exist = check_booking_exist(club['name'], competition['name'], bookings)

    # If exists retreiving datas
    if booking_exist:
        booking = [b for b in bookings if b['club'] == club['name']
                   and b['competition'] == competition['name']][0]
        max_booking = 12-int(booking['places'])
    else:
        # creation of the entry
        booking = {
            'club': club['name'],
            'competition': competition['name'],
            'places': "0"}
        bookings.append(booking)
        max_booking = 12

    placesRequired = int(request.form['places'])
    if placesRequired < 0:
        flash("You can't book a negative number of places !")
        return render_template('welcome.html', club=club, competitions=competitions)

    if not check_competion_is_open(competition['date']):
        flash('Competition closed !')
    else:
        if placesRequired > int(club['points']):
            flash('Not enough points !')
            points_ok = False
        if placesRequired > max_booking:
            flash(f'{max_booking} places maximum !')
            max_places_ok = False
        if (int(competition['numberOfPlaces'])-placesRequired) < 0:
            flash('You cant reserve that much places !')
            enough_places = False
        # Si tout est OK
        if (points_ok and max_places_ok and enough_places):
            competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
            club['points'] = int(club['points'])-placesRequired
            booking['places'] = int(booking['places'])+placesRequired
            flash('Great-booking complete!')
            print(bookings)

    return render_template('welcome.html', club=club, competitions=competitions)


# Added route for points display
@app.route('/points')
def display_clubs_points():
    return render_template('points.html', clubs=clubs)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
