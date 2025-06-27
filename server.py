from flask import Flask, render_template, request, redirect, flash, url_for
from utilities import loadClubs, loadCompetitions, checkMailExist


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def showSummary():
    if checkMailExist(request.form['email']):
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        return render_template('welcome.html', club=club, competitions=competitions)
    else:
        flash("Mail unknown, please retry")
        return render_template('index.html')


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    points_ok = True
    max_places_ok = True
    enough_places = True

    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])

    if placesRequired > int(club['points']):
        flash('Not enough points !')
        points_ok = False
    if placesRequired > 12:
        flash('12 places maximum !')
        max_places_ok = False
    if (int(competition['numberOfPlaces'])-placesRequired) < 0:
        flash('You cant reserve that much places !')
        enough_places = False
    if (points_ok and max_places_ok and enough_places):
        competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
        club['points'] = int(club['points'])-placesRequired
        flash('Great-booking complete!')

    return render_template('welcome.html', club=club, competitions=competitions)


# Added route for points display
@app.route('/points')
def display_clubs_points():
    return render_template('points.html', clubs=clubs)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
