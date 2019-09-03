# -*- coding: utf-8 -*-

"""This module allows to check REST vulnerabilities."""

# standard imports
import re

# third party imports
# None

# local imports
from fluidasserts import LOW, MEDIUM, DAST
from fluidasserts import show_close
from fluidasserts import show_open
from fluidasserts import show_unknown
from fluidasserts.proto.http import _has_insecure_value
from fluidasserts.utils.decorators import track, level, notify, api, unknown_if
from fluidasserts.helper import http

HDR_RGX = {
    'content-type': '^(\\s)*.+(\\/|-).+(\\s)*;(\\s)*charset.*$',
    'strict-transport-security': (r'^\s*max-age\s*=\s*'
                                  # 123 or "123" as a capture group
                                  r'"?((?<!")\d+(?!")|(?<=")\d+(?="))"?'),
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

    session._add_unit(
        is_vulnerable=is_vulnerable,
        source=f'HTTP/Response/Headers/{header}',
        specific=[header])

    return session._get_tuple_result(
        msg_open=f'Insecure header {header} is present',
        msg_closed=f'Insecure header {header} is not present')


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
