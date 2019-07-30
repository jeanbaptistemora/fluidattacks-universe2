# -*- coding: utf-8 -*-

"""This module allows to check REST vulnerabilities."""

# standard imports
import re

# third party imports
# None

# local imports
from fluidasserts import Result
from fluidasserts import OPEN, CLOSED, UNKNOWN
from fluidasserts import LOW, MEDIUM
from fluidasserts import show_close
from fluidasserts import show_open
from fluidasserts import show_unknown
from fluidasserts.proto.http import _has_insecure_value
from fluidasserts.utils.decorators import track, level, notify, api
from fluidasserts.helper import http

HDR_RGX = {
    'content-type': '^(\\s)*.+(\\/|-).+(\\s)*;(\\s)*charset.*$',
    'strict-transport-security': '^\\s*max-age=\\s*\\d+',
    'x-content-type-options': '^\\s*nosniff\\s*$',
    'x-frame-options': '^\\s*deny.*$',
}  # type: dict


@notify
@level('low')
@track
def has_access(url: str, *args, **kwargs) -> bool:
    r"""
    Check if HTTP access to given URL is possible (i.e. response 200 OK).

    :param url: URL to test.
    :param \*args: Optional arguments for :class:`HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`HTTPSession`.
    """
    http_session = http.HTTPSession(url, *args, **kwargs)
    ok_access_list = [200, 202, 204, 301, 302, 307]
    if http_session.response.status_code in ok_access_list:
        show_open('Access available to {}'.format(url))
        return True
    show_close('Access not available to {}'.format(url))
    return False


@notify
@level('low')
@track
def accepts_empty_content_type(url: str, *args, **kwargs) -> bool:
    r"""
    Check if given URL accepts empty Content-Type requests.

    :param url: URL to test.
    :param \*args: Optional arguments for :class:`HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`HTTPSession`.
    """
    if 'headers' in kwargs:
        if 'Content-Type' in kwargs['headers']:
            kwargs['headers'].pop('Content-Type', None)
    expected_codes = [406, 415]
    try:
        session = http.HTTPSession(url, *args, **kwargs)
    except http.ConnError as exc:
        show_unknown('URL {} returned error'.format(url),
                     details=dict(error=str(exc).replace(':', ',')))
        return False
    except http.ParameterError as exc:
        show_unknown('An invalid parameter was passed',
                     details=dict(url=url,
                                  error=str(exc).replace(':', ',')))
        return False
    if session.response.status_code not in expected_codes:
        show_open('URL {} accepts empty Content-Type requests'.
                  format(url))
        return True
    show_close('URL {} rejects empty Content-Type requests'.
               format(url))
    return False


@notify
@level('low')
@track
def accepts_insecure_accept_header(url: str, *args, **kwargs) -> bool:
    r"""
    Check if given URL accepts insecure Accept request header value.

    :param url: URL to test.
    :param \*args: Optional arguments for :class:`HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`HTTPSession`.
    """
    expected_codes = [406, 415]
    if 'headers' in kwargs:
        kwargs['headers'].update({'Accept': '*/*'})
    elif kwargs:
        kwargs['headers'] = {'Accept': '*/*'}
    else:
        kwargs = {'headers': {'Accept': '*/*'}}
    try:
        session = http.HTTPSession(url, *args, **kwargs)
    except http.ConnError as exc:
        show_unknown('URL {} returned error'.format(url),
                     details=dict(error=str(exc).replace(':', ',')))
        return False

    if session.response.status_code not in expected_codes:
        show_open('URL {} accepts insecure Accept request header value'.
                  format(url))
        return True
    show_close('URL {} rejects insecure Accept request header value'.
               format(url))
    return False


@api(risk=MEDIUM)
def is_header_x_frame_options_missing(url: str, *args, **kwargs) -> Result:
    r"""
    Check if X-Frame-Options HTTP header is properly set.

    :param url: URL to test.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    """
    header = 'X-Frame-Options'
    try:
        result = _has_insecure_value(url, header, *args, **kwargs)
        if result is None:
            return OPEN, (f'Header {header} is not set, which is insecure '
                          f'as it allows for a Click Jacking attack')
        if result:
            return OPEN, f'Header {header} has insecure value'
        return CLOSED, f'Header {header} has a secure value'
    except http.ConnError as exc:
        return UNKNOWN, f'There was an error: {exc}'
    except http.ParameterError as exc:
        return UNKNOWN, f'An invalid parameter was passed: {exc}'


@api(risk=LOW)
def is_header_x_content_type_options_missing(url: str, *args,
                                             **kwargs) -> Result:
    r"""
    Check if X-Content-Type-Options HTTP header is properly set.

    :param url: URL to test.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    """
    header = 'X-Content-Type-Options'
    try:
        result = _has_insecure_value(url, header, *args, **kwargs)
        if result is None:
            return OPEN, (f'Header {header} is not set, which is insecure '
                          f'as it does not dissable MIME Sniffing.')
        if result:
            return OPEN, f'Header {header} has insecure value'
        return CLOSED, f'Header {header} has a secure value'
    except http.ConnError as exc:
        return UNKNOWN, f'There was an error: {exc}'
    except http.ParameterError as exc:
        return UNKNOWN, f'An invalid parameter was passed: {exc}'


@notify
@level('medium')
@track
def is_header_hsts_missing(url: str, *args, **kwargs) -> bool:
    r"""
    Check if Strict-Transport-Security HTTP header is properly set.

    :param url: URL to test.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    """
    result = True
    try:
        http_session = http.HTTPSession(url, *args, **kwargs)
        headers_info = http_session.response.headers
        fingerprint = http_session.get_fingerprint()
    except http.ConnError as exc:
        show_unknown('Could not connect',
                     details=dict(url=url,
                                  error=str(exc).replace(':', ',')))
        return False
    except http.ParameterError as exc:
        show_unknown('An invalid parameter was passed',
                     details=dict(url=url,
                                  error=str(exc).replace(':', ',')))
        return False

    header = 'Strict-Transport-Security'
    if header in headers_info:
        value = headers_info[header]
        if re.match(HDR_RGX[header.lower()], value, re.IGNORECASE):
            hdr_attrs = value.split(';')
            max_age = list(filter(lambda x: x.startswith('max-age'),
                                  hdr_attrs))[0]
            max_age_val = max_age.split('=')[1]
            if int(max_age_val) >= 31536000:
                show_close('HTTP header {} is secure'.format(header),
                           details=dict(url=url,
                                        header=header,
                                        value=value,
                                        fingerprint=fingerprint))
                result = False
            else:
                show_open('{} HTTP header is insecure'.
                          format(header),
                          details=dict(url=url, header=header, value=value,
                                       fingerprint=fingerprint))
                result = True
        else:
            show_open('{} HTTP header is insecure'.
                      format(header),
                      details=dict(url=url, header=header, value=value,
                                   fingerprint=fingerprint))
            result = True
    return result


@api(risk=LOW)
def is_header_content_type_missing(url: str, *args, **kwargs) -> Result:
    r"""
    Check if Content-Type HTTP header is properly set.

    :param url: URL to test.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    """
    header = 'Content-Type'
    try:
        result = _has_insecure_value(url, header, *args, **kwargs)
        if result is None:
            return OPEN, (f'Header {header} is not set, which is insecure '
                          f'as it leaves the type of the response open '
                          f'to interpretation (which may introduce '
                          f'vulnerabilities by an improper synchronization '
                          f'between the client and the server, or sniffing '
                          f'of the payload.')
        if result:
            return OPEN, f'Header {header} has insecure value'
        return CLOSED, f'Header {header} has a secure value'
    except http.ConnError as exc:
        return UNKNOWN, f'There was an error: {exc}'
    except http.ParameterError as exc:
        return UNKNOWN, f'An invalid parameter was passed: {exc}'
