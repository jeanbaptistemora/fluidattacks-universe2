# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.proto.rest."""

# standard imports
# None

# 3rd party imports
import pytest
pytestmark = pytest.mark.proto

# local imports
from fluidasserts.proto import rest


# Constants

MOCK_SERVICE = 'http://localhost:5000'
NO_HEADERS = 'http://localhost:5000/noheaders'
BASE_URL = MOCK_SERVICE + '/rest'
BWAPP_PORT = 80
NONEXISTANT_SERVICE = 'http://nonexistant.fluidattacks.com'
BAD_FORMAT_SERVICE = 'fluidattacks'

#
# Open tests
#


def test_has_access_open():
    """Resource is available?."""
    assert rest.has_access(BASE_URL + '/access/fail')


def test_insecure_accept_open():
    """Resource is available?."""
    assert rest.accepts_insecure_accept_header(
        BASE_URL + '/insecure_accept/fail')


def test_hsts_open():
    """Header Strict-Transport-Security no establecido?."""
    assert rest.is_header_hsts_missing(
        '%s/hsts/fail' % (BASE_URL))


def test_frame_options_open():
    """Check X-Frame-Options header."""
    assert rest.is_header_x_frame_options_missing(NO_HEADERS).is_open()
    assert rest.is_header_x_frame_options_missing(
        '%s/frame_options/fail' % (BASE_URL)).is_open()


def test_content_options_open():
    """Check X-Content-Type-Options header."""
    assert rest.is_header_x_content_type_options_missing(NO_HEADERS).is_open()
    assert rest.is_header_x_content_type_options_missing(
        '%s/content_options/fail' % (BASE_URL)).is_open()


def test_content_type_open():
    """Check Content-Type header."""
    assert rest.is_header_content_type_missing(NO_HEADERS).is_open()
    assert rest.is_header_content_type_missing(
        '%s/content_type/fail' % (BASE_URL)).is_open()


def test_empty_content_type_open():
    """Check empty Content-Type."""
    assert rest.accepts_empty_content_type(
        '%s/empty_content_type/fail' % (BASE_URL))


#
# Closing tests
#


def test_has_access_close():
    """Resource is available?."""
    assert not rest.has_access(BASE_URL + '/access/ok')


def test_insecure_accept_close():
    """Resource is available?."""
    assert not rest.accepts_insecure_accept_header(
        BASE_URL + '/insecure_accept/ok',
        timeout=10)
    assert not rest.accepts_insecure_accept_header(
        NONEXISTANT_SERVICE + '/insecure_accept/ok',
        headers={'Accept': 'text/html'})


def test_hsts_close():
    """Header Strict-Transport-Security establecido?."""
    assert not rest.is_header_hsts_missing(
        '%s/hsts/ok' % (BASE_URL))
    assert not rest.is_header_hsts_missing(
        '%s/hsts/ok' % (NONEXISTANT_SERVICE))
    assert not rest.is_header_hsts_missing(
        '%s/hsts/ok' % (BAD_FORMAT_SERVICE))


def test_content_options_close():
    """Check X-Content-Type-Options header."""
    assert rest.is_header_x_content_type_options_missing(
        '%s/content_type/ok' % (BASE_URL)).is_closed()
    assert rest.is_header_x_content_type_options_missing(
        '%s/content_type/ok' % (NONEXISTANT_SERVICE)).is_unknown()
    assert rest.is_header_x_content_type_options_missing(
        '%s/content_type/ok' % (BAD_FORMAT_SERVICE)).is_unknown()


def test_empty_content_type_close():
    """Check empty Content-Type."""
    assert not rest.accepts_empty_content_type(
        '%s/empty_content_type/ok' % (BASE_URL),
        headers={'Content-Type': 'text/html'})
    assert not rest.accepts_empty_content_type(
        '%s/empty_content_type/ok' % (NONEXISTANT_SERVICE))
    assert not rest.accepts_empty_content_type(
        '%s/empty_content_type/ok' % (BAD_FORMAT_SERVICE))


def test_content_type_close():
    """Check Content-Type header."""
    assert rest.is_header_content_type_missing(
        '%s/content_type/ok' % (BASE_URL)).is_closed()
    assert rest.is_header_content_type_missing(
        '%s/content_type/ok' % (NONEXISTANT_SERVICE)).is_unknown()
    assert rest.is_header_content_type_missing(
        '%s/content_type/ok' % (BAD_FORMAT_SERVICE)).is_unknown()


def test_frame_options_close():
    """Check X-Frame-Options header."""
    assert rest.is_header_x_frame_options_missing(
        '%s/frame_options/ok' % (BASE_URL)).is_closed()
    assert rest.is_header_x_frame_options_missing(
        '%s/frame_options/ok' % (NONEXISTANT_SERVICE)).is_unknown()
    assert rest.is_header_x_frame_options_missing(
        '%s/frame_options/ok' % (BAD_FORMAT_SERVICE)).is_unknown()
