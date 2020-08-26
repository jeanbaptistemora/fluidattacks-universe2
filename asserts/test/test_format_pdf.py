# -*- coding: utf-8 -*-

"""Modulo para pruebas de PDF.

Este modulo contiene las funciones necesarias para probar si el modulo de
PDF se encuentra adecuadamente implementado.

El mock en este caso son archivos PDF intencionalmente construidos para
reflejar las vulnerabilidades y/o correcciones propias de un archivo
PDF.
"""

# standard imports
# none

# 3rd party imports
import pytest
pytestmark = pytest.mark.asserts_module('format')

# local imports
from fluidasserts.format import pdf


# Constants


#
# Open tests
#


def test_pdf_has_author_open():
    """PDF tiene metados de autor en el docinfo?."""
    assert pdf.has_author('test/static/format/pdf/vulnerable.pdf')


def test_pdf_has_creator_open():
    """PDF tiene metados de creador en el docinfo?."""
    assert pdf.has_creator('test/static/format/pdf/vulnerable.pdf')


def test_pdf_has_producer_open():
    """PDF tiene metados de productor en el docinfo?."""
    assert pdf.has_producer('test/static/format/pdf/vulnerable.pdf')


#
# Close tests
#


def test_pdf_has_author_close():
    """PDF no tiene metados de autor en el docinfo?."""
    assert not pdf.has_author('test/static/format/pdf/non-vulnerable.pdf')


def test_pdf_has_creator_close():
    """PDF no tiene metados de creador en el docinfo?."""
    assert not pdf.has_creator('test/static/format/pdf/non-vulnerable.pdf')


def test_pdf_has_producer_close():
    """PDF no tiene metados de productor en el docinfo?."""
    assert not pdf.has_producer('test/static/format/pdf/non-vulnerable.pdf')

# pendiente incluir soporte de metadata xdf
# pdf.has_create_date('test/vulnerable.pdf')
# pdf.has_modify_date('test/vulnerable.pdf')
# pdf.has_tagged('test/vulnerable.pdf')
# pdf.has_language('test/vulnerable.pdf')

# pendiente incluir soporte de metadata xdf
# pdf.has_create_date('test/non-vulnerable.pdf')
# pdf.has_modify_date('test/non-vulnerable.pdf')
# pdf.has_tagged('test/non-vulnerable.pdf')
# pdf.has_language('test/non-vulnerable.pdf')
