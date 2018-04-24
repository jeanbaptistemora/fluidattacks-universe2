# -*- coding: utf-8 -*-

"""CAPTCHA module."""


# standard imports
try:
    import Image
except ImportError:
    from PIL import Image

# 3rd party imports
import pytesseract

# local imports
from fluidasserts import show_close
from fluidasserts import show_open
from fluidasserts.helper import http_helper
from fluidasserts.utils.decorators import track


@track
def is_insecure_in_image(image, expected_text):
    """Check if the image is an insecure CAPTCHA."""
    result = pytesseract.image_to_string(Image.open(image))
    if result == expected_text:
        show_open('Captcha is insecure',
                  details=dict(expected=expected_text, reversed=result))
        return True
    show_close('Captcha is secure',
               details=dict(expected=expected_text, reversed=result))
    return False


@track
def is_insecure_in_url(image_url, expected_text, *args, **kwargs):
    """Check if the URL is an insecure CAPTCHA."""
    session = http_helper.HTTPSession(image_url, stream=True, *args, **kwargs)
    fingerprint = session.get_fingerprint()
    image = session.response.raw
    result = pytesseract.image_to_string(Image.open(image))
    if result == expected_text:
        show_open('Captcha is insecure',
                  details=dict(expected=expected_text, reversed=result,
                               fingerprint=fingerprint))
        return True
    show_close('Captcha is secure',
               details=dict(expected=expected_text, reversed=result,
                            fingerprint=fingerprint))
    return False
