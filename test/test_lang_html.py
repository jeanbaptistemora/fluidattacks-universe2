# -*- coding: utf-8 -*-

"""Modulo para pruebas de vulnerabilides en codigo HTML.

Este modulo contiene las funciones necesarias para probar si el modulo de
HTML se encuentra adecuadamente implementado.
"""

# standard imports

# 3rd party imports
import pytest
pytestmark = pytest.mark.asserts_module('lang')

# local imports
from fluidasserts.lang import html


# Constants


CODE_DIR = 'test/static/lang/html/'
SECURE_CODE = CODE_DIR + 'non-vulnerable.html'
INSECURE_CODE = CODE_DIR + 'vulnerable.html'
INSECURE_CODE2 = CODE_DIR + 'vulnerable2.html'
NOT_CODE = CODE_DIR + 'notexists.html'

#
# Open tests
#


def test_form_autocomplete_open():
    """Funcion test_form_autocomplete_open.

    Verifica si el atributo autocomplete=off se encuentra en el
    codigo HTML de vulnerable.html
    """
    assert html.has_not_autocomplete(INSECURE_CODE).is_open()
    assert html.has_not_autocomplete(INSECURE_CODE2).is_open()


def test_is_cacheable_open():
    """Funcion test_is_cacheable_open.

    Validar si las etiquetas que evitan que se almacene la pagina en
    memoria cache estan definidas en el codigo HTML de
    vulnerable.html
    """
    assert html.is_cacheable(INSECURE_CODE)


def test_is_header_content_type_missing_open():
    """Funcion test_is_header_content_type_missing_open.

    Validar si las etiquetas que establecen la cabecera Content-Type
    estan definidas en el codigo HTML de vulnerable.html
    """
    assert html.is_header_content_type_missing(INSECURE_CODE)


def test_open_has_reverse_tab_nabbing():
    """Test html.has_reverse_tabnabbing."""
    assert html.has_reverse_tabnabbing(CODE_DIR).is_open()
    assert html.has_reverse_tabnabbing(INSECURE_CODE).is_open()


def test_open_has_not_subresource_integrity():
    """Test html.has_not_subresource_integrity."""
    assert html.has_not_subresource_integrity(CODE_DIR).is_open()
    assert html.has_not_subresource_integrity(INSECURE_CODE).is_open()


#
# Closing tests
#


def test_form_autocomplete_close():
    """Funcion test_form_autocomplete_close.

    Verifica si el atributo autocomplete=off se encuentra en el
    codigo HTML de non-vulnerable.html?
    """
    assert not html.has_not_autocomplete(SECURE_CODE)
    assert not html.has_not_autocomplete(NOT_CODE)


def test_is_cacheable_close():
    """Funcion test_is_cacheable_close.

    Validar si las etiquetas que evitan que se almacene la pagina en
    memoria cache estan definidas en el codigo HTML de
    non-vulnerable.html
    """
    assert not html.is_cacheable(SECURE_CODE)
    assert not html.is_cacheable(NOT_CODE)


def test_is_header_content_type_missing_close():
    """Funcion test_is_header_content_type_missing_open.

    Validar si las etiquetas que establecen la cabecera Content-Type
    estan definidas en el codigo HTML de non-vulnerable.html
    """
    assert not html.is_header_content_type_missing(SECURE_CODE)
    assert not html.is_header_content_type_missing(NOT_CODE)


def test_closed_has_reverse_tab_nabbing():
    """Test html.has_reverse_tabnabbing."""
    assert html.has_reverse_tabnabbing(SECURE_CODE).is_closed()
    assert html.has_reverse_tabnabbing(NOT_CODE).is_unknown()


def test_closed_has_not_subresource_integrity():
    """Test html.has_not_subresource_integrity."""
    assert html.has_not_subresource_integrity(SECURE_CODE).is_closed()
    assert html.has_not_subresource_integrity(NOT_CODE).is_unknown()
