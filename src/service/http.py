# -*- coding: utf-8 -*-

"""Modulo para verificacion del protocolo HTTP.

Este modulo permite verificar vulnerabilidades propias de HTTP como:

    * Transporte plano de informacion,
    * Headers de seguridad no establecidos,
    * Cookies no generadas de forma segura,
"""

# standard imports
import logging
import re

# 3rd party imports
# None

# local imports
from fluidasserts.helper import banner_helper
from fluidasserts.helper import http_helper
from fluidasserts import show_close
from fluidasserts import show_open
from fluidasserts.utils.decorators import track

logger = logging.getLogger('FLUIDAsserts')


# pylint: disable=R0913
def generic_http_assert(url, expected_regex, *args, **kwargs):
    """Generic HTTP assert method."""
    http_session = http_helper.HTTPSession(url, *args, **kwargs)
    response = http_session.response
    the_page = response.text

    if re.search(str(expected_regex), the_page, re.IGNORECASE) is None:
        return False
    return True


@track
def has_text(url, expected_text, *args, **kwargs):
    """Check if a bad text is present."""
    ret = generic_http_assert(url, expected_text, *args, **kwargs)
    if ret:
        logger.info('%s: %s Bad text present, Details=%s',
                    show_open(), url, expected_text)
        return True
    else:
        logger.info('%s: %s Bad text not present, Details=%s',
                    show_close(), url, expected_text)
        return False


@track
def has_not_text(url, expected_text, *args, **kwargs):
    """Check if a required text is not present."""
    ret = generic_http_assert(url, expected_text, *args, **kwargs)
    if not ret:
        logger.info('%s: %s Expected text not present, Details=%s',
                    show_open(), url, expected_text)
        return True
    else:
        logger.info('%s: %s Expected text present, Details=%s',
                    show_close(), url, expected_text)
        return False


@track
def is_header_x_asp_net_version_missing(url):
    """Check if x-aspnet-version header is missing."""
    return http_helper.has_insecure_header(url, 'x-aspnet-version')


@track
def is_header_access_control_allow_origin_missing(url):
    """Check if access-control-allow-origin header is missing."""
    return http_helper.has_insecure_header(url,
                                           'access-control-allow-origin')


@track
def is_header_cache_control_missing(url):
    """Check if cache-control header is missing."""
    return http_helper.has_insecure_header(url, 'cache-control')


@track
def is_header_content_security_policy_missing(url):
    """Check if content-security-policy header is missing."""
    return http_helper.has_insecure_header(url,
                                           'content-security-policy')


@track
def is_header_content_type_missing(url):
    """Check if content-security-policy header is missing."""
    return http_helper.has_insecure_header(url, 'content-type')


@track
def is_header_expires_missing(url):
    """Check if content-security-policy header is missing."""
    return http_helper.has_insecure_header(url, 'expires')


@track
def is_header_pragma_missing(url):
    """Check if pragma header is missing."""
    return http_helper.has_insecure_header(url, 'pragma')


@track
def is_header_server_insecure(url):
    """Check if server header is insecure."""
    return http_helper.has_insecure_header(url, 'server')


@track
def is_header_x_content_type_options_missing(url):
    """Check if x-content-type-options header is missing."""
    return http_helper.has_insecure_header(url,
                                           'x-content-type-options')


@track
def is_header_x_frame_options_missing(url):
    """Check if x-frame-options header is missing."""
    return http_helper.has_insecure_header(url, 'x-frame-options')


@track
def is_header_perm_cross_dom_pol_missing(url):
    """Check if permitted-cross-domain-policies header is missing."""
    return http_helper.has_insecure_header(url,
                                           'permitted-cross-domain-policies')


@track
def is_header_x_xxs_protection_missing(url):
    """Check if x-xss-protection header is missing."""
    return http_helper.has_insecure_header(url, 'x-xss-protection')


@track
def is_header_hsts_missing(url):
    """Check if strict-transport-security header is missing."""
    return http_helper.has_insecure_header(url,
                                           'strict-transport-security')


@track
def is_basic_auth_enabled(url):
    """Check if BASIC authentication is enabled."""
    return http_helper.has_insecure_header(url,
                                           'www-authenticate')


@track
def has_trace_method(url):
    """Check HTTP TRACE."""
    return http_helper.has_method(url, 'TRACE')


@track
def has_delete_method(url):
    """Check HTTP DELETE."""
    return http_helper.has_method(url, 'DELETE')


@track
def has_put_method(url):
    """Check HTTP PUT."""
    return http_helper.has_method(url, 'PUT')


@track
def has_sqli(url, expect=None, *args, **kwargs):
    """Check SQLi vuln by checking expected string."""
    if expect is None:
        expect = 'OLE.*Provider.*error'

    return has_text(url, expect, *args, **kwargs)


@track
def has_xss(url, expect, *args, **kwargs):
    """Check XSS vuln by checking expected string."""
    return has_text(url, expect,  *args, **kwargs)


@track
def has_command_injection(url, expect, *args, **kwargs):
    """Check command injection vuln by checking expected string."""
    return has_text(url, expect, *args, **kwargs)


@track
def has_php_command_injection(url, expect, *args, **kwargs):
    """Check PHP command injection by checking expected string."""
    return has_text(url, expect, *args, **kwargs)


@track
def has_session_fixation(url, expect, *args, **kwargs):
    """Check session fixation by no passing cookies and authenticating."""
    return has_text(url, expect, *args, **kwargs)


@track
def has_insecure_dor(url, expect, *args, **kwargs):
    """Check insecure direct object reference vuln."""
    return has_text(url, expect, *args, **kwargs)


@track
def has_dirtraversal(url, expect, *args, **kwargs):
    """Check directory traversal vuln by checking expected string."""
    return has_text(url, expect, *args, **kwargs)


@track
def has_csrf(url, expect, *args, **kwargs):
    """Check CSRF vuln by checking expected string."""
    return has_text(url, expect, *args, **kwargs)


@track
def has_lfi(url, expect, *args, **kwargs):
    """Check local file inclusion vuln by checking expected string."""
    return has_text(url, expect, *args, **kwargs)


@track
def has_hpp(url, expect, *args, **kwargs):
    """Check HTTP Parameter Pollution vuln."""
    return has_text(url, expect, *args, **kwargs)


@track
def has_insecure_upload(url, expect, file_param, file_path, params=None,
                        data='', cookies=None):
    """Check insecure upload vuln."""
    exploit_file = {file_param: open(file_path)}
    return has_text(url, expect, params=params, data=data,
                    files=exploit_file, cookies=cookies)


@track
def is_sessionid_exposed(url, argument='sessionid', *args, **kwargs):
    """Check if resulting URL has a session ID exposed."""
    http_session = http_helper.HTTPSession(url, *args, **kwargs)
    response_url = http_session.response.url

    regex = r'\b' + argument + r'\b'

    result = True
    if re.search(regex, response_url):
        result = True
        logger.info('%s: Session ID is exposed in %s, Details=%s',
                    show_open(), response_url, argument)
    else:
        result = False
        logger.info('%s: Session ID is hidden in %s, Details=%s',
                    show_close(), response_url, argument)
    return result


@track
def is_version_visible(ip_address, ssl=False, port=80):
    """Check if banner is visible."""
    if ssl:
        service = banner_helper.HTTPSService()
    else:
        service = banner_helper.HTTPService()
    banner = banner_helper.get_banner(service, ip_address)
    version = banner_helper.get_version(service, banner)

    result = True
    if version:
        result = True
        logger.info('%s: HTTP version visible on %s:%s, Details=%s',
                    show_open(), ip_address, port, version)
    else:
        result = False
        logger.info('%s: HTTP version not visible on %s:%s, Details=None',
                    show_close(), ip_address, port)
    return result


@track
def is_not_https_required(url):
    """Check if HTTPS is always forced on a given url."""
    http_session = http_helper.HTTPSession(url)
    if http_session.url.startswith('https'):
        logger.info('%s: HTTPS is forced on URL, Details=%s',
                    show_close(), http_session.url)
        return False
    else:
        logger.info('%s: HTTPS is not forced on URL, Details=%s',
                    show_open(), http_session.url)
        return True


@track
def has_dirlisting(url):
    """Check if url has directory listing enabled."""
    bad_text = 'Index of'
    return has_text(url, bad_text)
