# -*- coding: utf-8 -*-

"""Modulo para pruebas de captcha."""

# standard imports
# None

# 3rd party imports
# None

# local imports
from fluidasserts.format import captcha


# Constants

SECURE_CAPTCHA_IMG = ['test/provision/captcha/secure.jpg', '504375']
WEAK_CAPTCHA_IMG = ['test/provision/captcha/weak.jpg', 'WORDS']
SECURE_CAPTCHA_URL = ['http://127.0.0.1:5000/static/secure.jpg', '504375']
WEAK_CAPTCHA_URL = ['http://127.0.0.1:5000/static/weak.jpg', 'WORDS']


#
# Open tests
#

def test_is_insecure_in_image_open():
    """Insecure captcha open."""
    assert captcha.is_insecure_in_image(WEAK_CAPTCHA_IMG[0],
                                        WEAK_CAPTCHA_IMG[1])


def test_is_insecure_in_url_open():
    """Insecure captcha open."""
    assert captcha.is_insecure_in_url(WEAK_CAPTCHA_URL[0],
                                      WEAK_CAPTCHA_URL[1])

#
# Closing tests
#

def test_is_insecure_in_image_close():
    """Insecure captcha close."""
    assert captcha.is_insecure_in_image(SECURE_CAPTCHA_IMG[0],
                                        SECURE_CAPTCHA_IMG[1]).is_closed()
    assert captcha.is_insecure_in_url('not exists', 'test').is_unknown()


def test_is_insecure_in_url_close():
    """Insecure captcha close."""
    assert captcha.is_insecure_in_url(SECURE_CAPTCHA_URL[0],
                                      SECURE_CAPTCHA_URL[1]).is_closed()
    assert captcha.is_insecure_in_url('param error', 'test').is_unknown()
    assert captcha.is_insecure_in_url('http://0.0.0.0', 'test').is_unknown()
