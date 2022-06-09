# -*- coding: utf-8 -*-

"""Modulo para pruebas de vulnerabilides en codigo HTML.

Este modulo contiene las funciones necesarias para probar si el modulo de
HTML se encuentra adecuadamente implementado.
"""


import pytest

pytestmark = pytest.mark.asserts_module("lang_html")


from fluidasserts.lang import (
    html,
)

# Constants


CODE_DIR = "test/static/lang/html/"
SECURE_CODE = CODE_DIR + "non-vulnerable.html"
INSECURE_CODE = CODE_DIR + "vulnerable.html"
INSECURE_CODE2 = CODE_DIR + "vulnerable2.html"
NOT_CODE = CODE_DIR + "notexists.html"

#
# Open tests
#


def test_is_header_content_type_missing_open():
    """Funcion test_is_header_content_type_missing_open.

    Validar si las etiquetas que establecen la cabecera Content-Type
    estan definidas en el codigo HTML de vulnerable.html
    """
    assert html.is_header_content_type_missing(INSECURE_CODE)
    assert html.is_header_content_type_missing(
        CODE_DIR + "content_type_weak.html"
    )


def test_open_has_not_subresource_integrity():
    """Test html.has_not_subresource_integrity."""
    assert html.has_not_subresource_integrity(CODE_DIR).is_open()
    assert html.has_not_subresource_integrity(INSECURE_CODE).is_open()


#
# Closing tests
#


def test_is_header_content_type_missing_close():
    """Funcion test_is_header_content_type_missing_open.

    Validar si las etiquetas que establecen la cabecera Content-Type
    estan definidas en el codigo HTML de non-vulnerable.html
    """
    assert not html.is_header_content_type_missing(SECURE_CODE)
    assert not html.is_header_content_type_missing(NOT_CODE)
    assert not html.is_header_content_type_missing(
        CODE_DIR + "content_type_safe.html"
    )


def test_closed_has_not_subresource_integrity():
    """Test html.has_not_subresource_integrity."""
    assert html.has_not_subresource_integrity(SECURE_CODE).is_closed()
    assert html.has_not_subresource_integrity(NOT_CODE).is_unknown()
