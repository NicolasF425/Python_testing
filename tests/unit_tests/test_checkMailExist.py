from utilities import check_mail_exist


def test_checkMailExist_OK():
    test_mail = "john@simplylift.co"
    result = check_mail_exist(test_mail)

    assert result


def test_checkMailExist_KO():
    test_mail = "toto@toto.com"
    result = check_mail_exist(test_mail)

    assert result is not True
