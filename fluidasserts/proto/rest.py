# -*- coding: utf-8 -*-

"""This module allows to check REST vulnerabilities."""

# standard imports
import re
from typing import Dict

# third party imports
# None

# local imports
from fluidasserts import LOW, MEDIUM, DAST
from fluidasserts.helper import http
from fluidasserts.proto.http import _has_insecure_value
from fluidasserts.utils.decorators import api, unknown_if

HDR_RGX: Dict[str, str] = {
    'content-type': '^(\\s)*.+(\\/|-).+(\\s)*;(\\s)*charset.*$',
    'strict-transport-security': (r'^\s*max-age\s*=\s*'
                                  # 123 or "123" as a capture group
                                  r'"?((?<!")\d+(?!")|(?<=")\d+(?="))"?'),
    'x-content-type-options': '^\\s*nosniff\\s*$',
    'x-frame-options': '^\\s*deny.*$',
}


@api(risk=LOW, kind=DAST)
@unknown_if(http.ParameterError, http.ConnError)
def has_access(url: str, *args, **kwargs) -> tuple:
    r"""
    Check if HTTP access to given URL is possible (i.e. response 200 OK).

    :param url: URL to test.
    :param \*args: Optional arguments for :class:`HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`HTTPSession`.
    :rtype: :class:`fluidasserts.Result`
    """
    ok_access_list = (200, 202, 204, 301, 302, 307)
    session = http.HTTPSession(url, *args, **kwargs)
    session.set_messages(
        source=f'REST/Response',
        msg_open='Endpoint is accessible',
        msg_closed='Endpoint is not accessible')
    session.add_unit(
        is_vulnerable=session.response.status_code in ok_access_list)
    return session.get_tuple_result()


@api(risk=LOW, kind=DAST)
@unknown_if(http.ParameterError, http.ConnError)
def accepts_empty_content_type(url: str, *args, **kwargs) -> tuple:
    r"""
    Check if given URL accepts empty Content-Type requests.

    :param url: URL to test.
    :param \*args: Optional arguments for :class:`HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`HTTPSession`.
    :rtype: :class:`fluidasserts.Result`
    """
    if 'headers' in kwargs:
        if 'Content-Type' in kwargs['headers']:
            kwargs['headers'].pop('Content-Type', None)

    session = http.HTTPSession(url, *args, **kwargs)
    session.set_messages(
        source=f'REST/Request/Headers/Content-Type',
        msg_open='Endpoint accepts empty Content-Type requests',
        msg_closed='Endpoint rejects empty Content-Type requests')
    session.add_unit(
        is_vulnerable=session.response.status_code not in (406, 415))
    return session.get_tuple_result()


@api(risk=LOW, kind=DAST)
@unknown_if(http.ParameterError, http.ConnError)
def accepts_insecure_accept_header(url: str, *args, **kwargs) -> tuple:
    r"""
    Check if given URL accepts insecure Accept request header value.

    :param url: URL to test.
    :param \*args: Optional arguments for :class:`HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`HTTPSession`.
    :rtype: :class:`fluidasserts.Result`
    """
    if 'headers' in kwargs:
        kwargs['headers'].update({'Accept': '*/*'})
    elif kwargs:
        kwargs['headers'] = {'Accept': '*/*'}
    else:
        kwargs = {'headers': {'Accept': '*/*'}}

    session = http.HTTPSession(url, *args, **kwargs)
    session.set_messages(
        source=f'REST/Request/Headers/Accept',
        msg_open='Endpoint accepts insecure Accept header requests',
        msg_closed='Endpoint rejects insecure Accept header requests')
    session.add_unit(
        is_vulnerable=session.response.status_code not in (406, 415))
    return session.get_tuple_result()


@api(risk=MEDIUM, kind=DAST)
def is_header_x_frame_options_missing(url: str, *args, **kwargs) -> tuple:
    r"""
    Check if X-Frame-Options HTTP header is properly set.

    :param url: URL to test.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    :rtype: :class:`fluidasserts.Result`
    """
    return _has_insecure_value(url, 'X-Frame-Options', True, *args, **kwargs)


@api(risk=LOW, kind=DAST)
def is_header_x_content_type_options_missing(url: str, *args,
                                             **kwargs) -> tuple:
    r"""
    Check if X-Content-Type-Options HTTP header is properly set.

    :param url: URL to test.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    :rtype: :class:`fluidasserts.Result`
    """
    return _has_insecure_value(
        url, 'X-Content-Type-Options', True, *args, **kwargs)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(http.ParameterError, http.ConnError)
def is_header_hsts_missing(url: str, *args, **kwargs) -> tuple:
    r"""
    Check if Strict-Transport-Security HTTP header is properly set.

    :param url: URL to test.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    :rtype: :class:`fluidasserts.Result`
    """
    header = 'Strict-Transport-Security'
    session = http.HTTPSession(url, *args, **kwargs)

    is_vulnerable: bool = True

    if header in session.response.headers:
        re_match = re.search(
            pattern=HDR_RGX[header.lower()],
            string=session.response.headers[header],
            flags=re.IGNORECASE)
        if re_match:
            max_age_val = re_match.groups()[0]
            if int(max_age_val) >= 31536000:
                is_vulnerable = False

    session.set_messages(
        source=f'REST/Response/Headers/{header}',
        msg_open=f'{header} is secure',
        msg_closed=f'{header} is insecure')
    session.add_unit(
        is_vulnerable=is_vulnerable)
    return session.get_tuple_result()


@api(risk=LOW, kind=DAST)
def is_header_content_type_missing(url: str, *args, **kwargs) -> tuple:
    r"""
    Check if Content-Type HTTP header is properly set.

    :param url: URL to test.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    :rtype: :class:`fluidasserts.Result`
    """
    return _has_insecure_value(url, 'Content-Type', True, *args, **kwargs)
