# -*- coding: utf-8 -*-

"""This module allows to check ``CAPTCHA`` vulnerabilities."""


# standard imports
from PIL import Image

# 3rd party imports
import pytesseract

# local imports
from fluidasserts import SAST, DAST, MEDIUM, _get_result_as_tuple_sast
from fluidasserts.helper import http
from fluidasserts.utils.decorators import unknown_if, api


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def is_insecure_in_image(image: str, expected_text: str) -> tuple:
    """
    Check if the given image is an insecure CAPTCHA.

    The check is performed by converting the image to text and
    comparing with the given expected text.

    :param image: Path to the image to be tested.
    :param expected_text: Text the image might contain.
    """
    image_obj = Image.open(image)

    ocr_result: str = pytesseract.image_to_string(image_obj)

    is_solvable_by_an_ocr: bool = ocr_result == expected_text

    return _get_result_as_tuple_sast(
        path=image,
        msg_open='Captcha is reversible by an OCR',
        msg_closed='Captcha is safe against an OCR',
        open_if=is_solvable_by_an_ocr)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(http.ConnError, http.ParameterError)
def is_insecure_in_url(image_url: str, expected_text: str,
                       *args, **kwargs) -> tuple:
    r"""
    Check if the image in the URL is an insecure CAPTCHA.

    The check is performed by converting the image to text and
    comparing with the given expected text.

    :param image_url: Path to the image to be tested.
    :param expected_text: Text the image might contain.
    :param \*args: Optional positional arguments for
        :class:`~fluidasserts.helper.http.HTTPSession`.
    :param \*\*kwargs: Optional keyword arguments for
        :class:`~fluidasserts.helper.http.HTTPSession`.
    """
    kwargs = kwargs or {}
    kwargs.update({'stream': True})
    session = http.HTTPSession(image_url, *args, **kwargs)
    session.set_messages(
        source='Captcha/Challenge/Complexity',
        msg_open='Captcha is reversible by an OCR',
        msg_closed='Captcha is safe against an OCR')

    image = session.response.raw
    image_obj = Image.open(image)

    ocr_result: str = pytesseract.image_to_string(image_obj)

    session.add_unit(is_vulnerable=ocr_result == expected_text)
    return session.get_tuple_result()
