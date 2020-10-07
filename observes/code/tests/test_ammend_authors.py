from code import ammend_authors


def test_get_mailmap_dict():
    mailmap_path = 'tests/mock_data/.mailmap'
    result = ammend_authors.get_mailmap_dict(mailmap_path)
    canon = ('Super Developer', 'sdev@canon.email.com')
    expected = {
        ('Super Developer', 'sdev95@flu-id.la'): canon,
        ('SDEV', 'sdev@canon.email.com'): canon,
        ('s.Dev-super V95', 'sdev95@alias.email.la'): canon,
        ('Super-Developer', 'sdev@other-domain'): canon,
    }
    assert expected == result
