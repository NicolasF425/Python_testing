from utilities import checkMailExist


def test_checkMailExist():
    test_mail = "john@simplylift.co"
    result = checkMailExist(test_mail)

    assert result
