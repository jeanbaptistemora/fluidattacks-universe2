# -*- coding: utf-8 -*-

"""This module allows to check PDF vulnerabilities."""

# 3rd party imports
from PyPDF2 import PdfFileReader

# local imports
from fluidasserts import Unit, SAST, LOW, OPEN, CLOSED
from fluidasserts.utils.decorators import api, unknown_if


@unknown_if(FileNotFoundError)
def _has_attribute(filename: str, metaname: str) -> tuple:
    """
    Check if ``docinfo`` attribute is present.

    :param filename: Path to the ``PDF`` file.
    :param metaname: Name of the attribute to search.
    """
    with open(filename, 'rb') as pdf_handle:
        input_pdf = PdfFileReader(pdf_handle)
        pdf_docinfo = input_pdf.getDocumentInfo()

    metavalue = getattr(pdf_docinfo, metaname)

    msg_open: str = f'{metaname} is present in PDF'
    msg_closed: str = f'{metaname} is not present in PDF'

    unit: Unit = Unit(where=filename,
                      specific=[msg_open if metavalue else msg_closed])

    if metavalue:
        return OPEN, msg_open, [unit], []
    return CLOSED, msg_closed, [], [unit]


@api(risk=LOW, kind=SAST)
def has_creator(filename: str) -> tuple:
    """
    Check if ``creator`` attribute is present.

    :param filename: Path to the ``PDF`` file.
    """
    return _has_attribute(filename, 'creator')


@api(risk=LOW, kind=SAST)
def has_producer(filename: str) -> tuple:
    """
    Check if ``producer`` attribute is present.

    :param filename: Path to the ``PDF`` file.
    """
    return _has_attribute(filename, 'producer')


@api(risk=LOW, kind=SAST)
def has_author(filename: str) -> tuple:
    """
    Check if ``author`` attribute is present.

    :param filename: Path to the ``PDF`` file.
    """
    return _has_attribute(filename, 'author')
