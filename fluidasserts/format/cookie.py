# -*- coding: utf-8 -*-

"""This module allows to check Cookies vulnerabilities."""


# standard imports
from typing import Optional

# 3rd party imports
from requests.cookies import RequestsCookieJar

# local imports
from fluidasserts import MEDIUM, DAST
from fluidasserts.helper import http
from fluidasserts.utils.decorators import api, unknown_if


@unknown_if(AssertionError, http.ConnError)
def _generic_check_attribute(cookie_attribute: str,
                             cookie_name: str,
                             url: Optional[str],
                             cookie_jar: Optional[RequestsCookieJar],
                             *args, **kwargs) -> tuple:
    r"""
    Check if a cookie has set to a secure value the provided attribute.

    Either **url** or **cookie_jar** has to be **None**.

    :param cookie_attribute: Attribute of the Cookie to test.
    :param cookie_name: Name of the cookie to test.
    :param url: URL to get cookies.
    :param cookie_jar: Collection of cookies as returned by
                       the **requests** package, please see
                       :class:`requests.cookies.RequestsCookieJar`.
    :param \*args: Optional positional arguments for
                   :class:`~fluidasserts.helper.http.HTTPSession`.
    :param \*\*kwargs: Optional keyword arguments for
                       :class:`~fluidasserts.helper.http.HTTPSession`.
    """
    kwargs = kwargs or {}
    kwargs.update({'request_at_instantiation': False})

    session = http.HTTPSession(url, *args, **kwargs)

    if url is not None:
        session.do_request()
        cookielist = session.cookies
    else:
        cookielist = cookie_jar

    session._set_messages(
        source=f'Cookie/Attributes/{cookie_attribute}',
        msg_open=f'{cookie_attribute} not set in cookie {cookie_name}',
        msg_closed=f'{cookie_attribute} is set in cookie {cookie_name}')

    if cookielist is None:
        raise AssertionError(f'Cookie is not present {cookie_name}')

    if not any(c.name == cookie_name for c in cookielist):
        raise AssertionError(f'Cookie {cookie_name} not found')

    is_vulnerable: bool = True

    for cookie in cookielist:
        if cookie.name != cookie_name:
            continue

        if cookie_attribute == 'HttpOnly' and (
                cookie.has_nonstandard_attr('HttpOnly') or
                cookie.has_nonstandard_attr('httponly')):
            is_vulnerable = False
        elif cookie_attribute == 'Secure' and \
                cookie.secure:
            is_vulnerable = False
        elif cookie_attribute == 'SameSite' and \
                cookie.get_nonstandard_attr('SameSite') == 'Strict':
            is_vulnerable = False

    session._add_unit(is_vulnerable=is_vulnerable)

    return session._get_tuple_result()


@api(risk=MEDIUM, kind=DAST)
def has_not_httponly_set(cookie_name: str, url: str, *args, **kwargs) -> tuple:
    r"""
    Check if the cookie in the **url** has the **HttpOnly** attribute.

    :param cookie_name: Name of the cookie to test.
    :param url: URL to get cookies.
    :param \*args: Optional positional arguments for
                   :class:`~fluidasserts.helper.http.HTTPSession`.
    :param \*\*kwargs: Optional keyword arguments for
                       :class:`~fluidasserts.helper.http.HTTPSession`.
    :returns: - ``OPEN`` if the specified cookie has not the HttpOnly
                attribute set.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    return _generic_check_attribute(
        'HttpOnly', cookie_name, url, None, *args, **kwargs)


@api(risk=MEDIUM, kind=DAST)
def has_not_httponly_in_cookiejar(
        cookie_name: str,
        cookie_jar: RequestsCookieJar) -> tuple:
    r"""
    Check if the cookie in the **cookie_jar** has the **HttpOnly** attribute.

    :param cookie_name: Name of the cookie to test.
    :param cookie_jar: Collection of cookies as returned by
                       the **requests** package, please see
                       :class:`requests.cookies.RequestsCookieJar`.
    :returns: - ``OPEN`` if the specified cookie has not the HttpOnly
                attribute set.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    return _generic_check_attribute('HttpOnly', cookie_name, None, cookie_jar)


@api(risk=MEDIUM, kind=DAST)
def has_not_secure_set(cookie_name: str, url: str, *args, **kwargs) -> bool:
    r"""
    Check if the cookie in the **url** has the **secure** attribute.

    :param cookie_name: Name of the cookie to test.
    :param url: URL to get cookies.
    :param \*args: Optional positional arguments for
                   :class:`~fluidasserts.helper.http.HTTPSession`.
    :param \*\*kwargs: Optional keyword arguments for
                       :class:`~fluidasserts.helper.http.HTTPSession`.
    :returns: - ``OPEN`` if the specified cookie has not the Secure
                attribute set.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    return _generic_check_attribute(
        'Secure', cookie_name, url, None, *args, **kwargs)


@api(risk=MEDIUM, kind=DAST)
def has_not_secure_in_cookiejar(cookie_name: str,
                                cookie_jar: RequestsCookieJar) -> bool:
    r"""
    Check if the cookie in the **cookie_jar** has the **secure** attribute set.

    :param cookie_name: Name of the cookie to test.
    :param cookie_jar: Collection of cookies as returned by
                       the **requests** package, please see
                       :class:`requests.cookies.RequestsCookieJar`.
    :returns: - ``OPEN`` if the specified cookie has not the Secure
                attribute set.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    return _generic_check_attribute('Secure', cookie_name, None, cookie_jar)


@api(risk=MEDIUM, kind=DAST)
def has_not_samesite_set(cookie_name: str, url: str, *args, **kwargs) -> bool:
    r"""
    Check if the cookie in the **url** has the **samesite** attribute.

    :param cookie_name: Name of the cookie to test.
    :param url: URL to get cookies.
    :param \*args: Optional positional arguments for
                   :class:`~fluidasserts.helper.http.HTTPSession`.
    :param \*\*kwargs: Optional keyword arguments for
                       :class:`~fluidasserts.helper.http.HTTPSession`.
    :returns: - ``OPEN`` if the specified cookie has not the SameSite
                attribute set.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    return _generic_check_attribute(
        'SameSite', cookie_name, url, None, *args, **kwargs)


@api(risk=MEDIUM, kind=DAST)
def has_not_samesite_in_cookiejar(cookie_name: str,
                                  cookie_jar: RequestsCookieJar) -> bool:
    r"""
    Check if the cookie in the **cookie_jar** has the **samesite** attribute.

    :param cookie_name: Name of the cookie to test.
    :param cookie_jar: Collection of cookies as returned by
                       the **requests** package, please see
                       :class:`requests.cookies.RequestsCookieJar`.
    :returns: - ``OPEN`` if the specified cookie has not the SameSite
                attribute set.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    return _generic_check_attribute('SameSite', cookie_name, None, cookie_jar)
