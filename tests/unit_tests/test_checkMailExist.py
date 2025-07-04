from utilities import checkMailExist


def test_checkMailExist_OK():
    test_mail = "john@simplylift.co"
    result = checkMailExist(test_mail)

    assert result


def test_checkMailExist_KO():
    test_mail = "toto@toto.com"
    result = checkMailExist(test_mail)

    assert result is not True
