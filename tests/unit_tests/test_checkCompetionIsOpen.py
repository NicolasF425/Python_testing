from utilities import checkCompetionIsOpen


def test_checkCompetionIsOpen_OK():
    date_competition = "2040-03-27 10:00:00"
    result = checkCompetionIsOpen(date_competition)

    assert result


def test_checkCompetionIsOpen_KO():
    date_competition = "2020-03-27 10:00:00"
    result = checkCompetionIsOpen(date_competition)

    assert result is False
