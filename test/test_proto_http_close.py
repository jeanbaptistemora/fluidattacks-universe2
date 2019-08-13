# -*- coding: utf-8 -*-

"""Modulo para pruebas de HTTP.

Este modulo contiene las funciones necesarias para probar si el modulo de
HTTP se encuentra adecuadamente implementado.
"""

# standard imports
from __future__ import print_function

# 3rd party imports
import pytest

# local imports
from fluidasserts.helper import http as helper
from fluidasserts.proto import http


#
# Constants
#

MOCK_SERVICE = 'http://localhost:5000'
NO_HEADERS = 'http://localhost:5000/noheaders'
BASE_URL = MOCK_SERVICE + '/http/headers'
BWAPP_PORT = 80
NONEXISTANT_SERVICE = 'http://nonexistant.fluidattacks.com'
BAD_FORMAT_SERVICE = 'fluidattacks'


def get_bwapp_cookies(cont_ip):
    """Log in to bWAPP and return valid cookie."""
    install_url = 'http://' + cont_ip + '/install.php?install=yes'
    helper.HTTPSession(install_url)
    login_url = 'http://' + cont_ip + '/login.php'
    http_session = helper.HTTPSession(login_url)

    http_session.data = 'login=bee&password=bug&security_level=0&form=submit'

    successful_text = 'Welcome Bee'
    http_session.formauth_by_response(successful_text)

    if not http_session.is_auth:
        return {}
    return http_session.cookies

#
# Close tests
#


@pytest.mark.parametrize('get_mock_ip', ['bwapp'], indirect=True)
def test_a1_sqli_close(get_mock_ip):
    """App vulnerable a SQLi?."""
    bwapp_cookie = get_bwapp_cookies(get_mock_ip)
    bwapp_cookie['security_level'] = '2'

    vulnerable_url = 'http://' + get_mock_ip + '/sqli_1.php'
    params = {'title': 'a\'', 'action': 'search'}

    assert not http.has_sqli(vulnerable_url, params, cookies=bwapp_cookie)
    assert not http.has_sqli(NONEXISTANT_SERVICE, params, cookies=bwapp_cookie)
    assert not http.has_sqli(BAD_FORMAT_SERVICE, params, cookies=bwapp_cookie)
    assert not http.has_sqli('%s/response/fail' % (MOCK_SERVICE),
                             params, cookies=bwapp_cookie)


@pytest.mark.parametrize('get_mock_ip', ['bwapp'], indirect=True)
def test_a1_os_injection_close(get_mock_ip):
    """App vulnerable a command injection?."""
    bwapp_cookie = get_bwapp_cookies(get_mock_ip)
    bwapp_cookie['security_level'] = '2'

    vulnerable_url = 'http://' + get_mock_ip + '/commandi.php'

    data = {'target': 'www.nsa.gov;uname', 'form': 'submit'}

    expected = 'uname'

    assert not http.has_command_injection(vulnerable_url, expected,
                                          data=data,
                                          cookies=bwapp_cookie)
    assert not http.has_command_injection(NONEXISTANT_SERVICE, expected,
                                          data=data,
                                          cookies=bwapp_cookie)
    assert not http.has_command_injection(BAD_FORMAT_SERVICE, expected,
                                          data=data,
                                          cookies=bwapp_cookie)


@pytest.mark.parametrize('get_mock_ip', ['bwapp'], indirect=True)
def test_a1_php_injection_close(get_mock_ip):
    """App vulnerable a PHP injection?."""
    bwapp_cookie = get_bwapp_cookies(get_mock_ip)
    bwapp_cookie['security_level'] = '2'

    vulnerable_url = 'http://' + get_mock_ip + '/phpi.php'

    params = {'message': 'test;phpinfo();'}

    expected = '<p><i>test;phpinfo()'

    assert http.has_php_command_injection(vulnerable_url, expected,
                                          params=params,
                                          cookies=bwapp_cookie)
    assert not http.has_php_command_injection(NONEXISTANT_SERVICE, expected,
                                              params=params,
                                              cookies=bwapp_cookie)
    assert not http.has_php_command_injection(BAD_FORMAT_SERVICE, expected,
                                              params=params,
                                              cookies=bwapp_cookie)


@pytest.mark.parametrize('get_mock_ip', ['bwapp'], indirect=True)
def test_a1_hpp_close(get_mock_ip):
    """App vulnerable a HTTP Parameter Polluiton?."""
    bwapp_cookie = get_bwapp_cookies(get_mock_ip)
    bwapp_cookie['security_level'] = '2'

    vulnerable_url = 'http://' + get_mock_ip + \
        '/hpp-3.php?movie=6&movie=7&movie=8&name=pepe&action=vote'

    expected = 'HTTP Parameter Pollution detected'

    assert http.has_hpp(vulnerable_url, expected, cookies=bwapp_cookie)
    assert not http.has_hpp(NONEXISTANT_SERVICE, expected,
                            cookies=bwapp_cookie)
    assert not http.has_hpp(BAD_FORMAT_SERVICE, expected,
                            cookies=bwapp_cookie)


@pytest.mark.parametrize('get_mock_ip', ['bwapp'], indirect=True)
def test_a1_insecure_upload_close(get_mock_ip):
    """App vulnerable a insecure upload?."""
    bwapp_cookie = get_bwapp_cookies(get_mock_ip)
    bwapp_cookie['security_level'] = '2'

    vulnerable_url = 'http://' + get_mock_ip + '/unrestricted_file_upload.php'

    file_param = 'file'
    file_path = 'test/provision/bwapp/exploit.php'
    data = {'MAX_FILE_SIZE': '100000', 'form': 'upload'}

    expected = 'Sorry, the file extension is not allowed'

    assert http.has_insecure_upload(vulnerable_url, expected,
                                    file_param, file_path, data=data,
                                    cookies=bwapp_cookie)
    assert not http.has_insecure_upload(NONEXISTANT_SERVICE, expected,
                                        file_param, file_path, data=data,
                                        cookies=bwapp_cookie)
    assert not http.has_insecure_upload(BAD_FORMAT_SERVICE, expected,
                                        file_param, file_path, data=data,
                                        cookies=bwapp_cookie)


@pytest.mark.parametrize('get_mock_ip', ['bwapp'], indirect=True)
def test_a2_sessionid_exposed_close(get_mock_ip):
    """Session ID expuesto?."""
    bwapp_cookie = get_bwapp_cookies(get_mock_ip)
    bwapp_cookie['security_level'] = '2'

    vulnerable_url = 'http://' + get_mock_ip + '/smgmt_sessionid_url.php'

    assert not http.is_sessionid_exposed(vulnerable_url,
                                         argument='PHPSESSID',
                                         cookies=bwapp_cookie)
    assert not http.is_sessionid_exposed(NONEXISTANT_SERVICE,
                                         argument='PHPSESSID',
                                         cookies=bwapp_cookie)
    assert not http.is_sessionid_exposed(BAD_FORMAT_SERVICE,
                                         argument='PHPSESSID',
                                         cookies=bwapp_cookie)


def test_a2_session_fixation_close():
    """Session fixation posible?."""
    assert http.has_session_fixation(
        '%s/session_fixation_close' % (BASE_URL), 'Login required')
    assert not http.has_session_fixation(
        '%s/session_fixation_close' % (NONEXISTANT_SERVICE), 'Login required')
    assert not http.has_session_fixation(
        '%s/session_fixation_close' % (BAD_FORMAT_SERVICE), 'Login required')


@pytest.mark.parametrize('get_mock_ip', ['bwapp'], indirect=True)
def test_a3_xss_close(get_mock_ip):
    """App vulnerable a XSS?."""
    bwapp_cookie = get_bwapp_cookies(get_mock_ip)
    bwapp_cookie['security_level'] = '2'

    vulnerable_url = 'http://' + get_mock_ip + \
        '/xss_get.php'
    params = {'firstname': '<script>alert(1)</script>',
              'lastname': 'b', 'form': 'submit'}

    expected = 'Welcome &lt;script'

    assert http.has_xss(vulnerable_url, expected, params,
                        cookies=bwapp_cookie)

    assert not http.has_xss(NONEXISTANT_SERVICE, expected, params,
                            cookies=bwapp_cookie)
    assert not http.has_xss(BAD_FORMAT_SERVICE, expected, params,
                            cookies=bwapp_cookie)


@pytest.mark.parametrize('get_mock_ip', ['bwapp'], indirect=True)
def test_a4_insecure_dor_close(get_mock_ip):
    """App vulnerable a direct object reference?."""
    bwapp_cookie = get_bwapp_cookies(get_mock_ip)
    bwapp_cookie['security_level'] = '2'

    vulnerable_url = 'http://' + get_mock_ip + \
        '/insecure_direct_object_ref_2.php'

    data = {'ticket_quantity': '1', 'ticket_price': '31337',
            'action': 'order'}

    expected = '<b>15 EUR</b>'

    assert http.has_insecure_dor(vulnerable_url, expected, data=data,
                                 cookies=bwapp_cookie)
    assert not http.has_insecure_dor(NONEXISTANT_SERVICE, expected, data=data,
                                     cookies=bwapp_cookie)
    assert not http.has_insecure_dor(BAD_FORMAT_SERVICE, expected, data=data,
                                     cookies=bwapp_cookie)


@pytest.mark.parametrize('get_mock_ip', ['bwapp'], indirect=True)
def test_a7_dirtraversal_close(get_mock_ip):
    """App vulnerable a directory traversal?."""
    bwapp_cookie = get_bwapp_cookies(get_mock_ip)
    bwapp_cookie['security_level'] = '2'

    vulnerable_url = 'http://' + get_mock_ip + '/directory_traversal_2.php'

    params = {'directory': '../'}

    expected = 'An error occurred, please try again'

    assert http.has_dirtraversal(vulnerable_url, expected,
                                 params=params,
                                 cookies=bwapp_cookie)
    assert not http.has_dirtraversal(NONEXISTANT_SERVICE, expected,
                                     params=params,
                                     cookies=bwapp_cookie)
    assert not http.has_dirtraversal(BAD_FORMAT_SERVICE, expected,
                                     params=params,
                                     cookies=bwapp_cookie)


@pytest.mark.parametrize('get_mock_ip', ['bwapp'], indirect=True)
def test_a7_lfi_close(get_mock_ip):
    """App vulnerable a LFI?."""
    bwapp_cookie = get_bwapp_cookies(get_mock_ip)
    bwapp_cookie['security_level'] = '2'

    vulnerable_url = 'http://' + get_mock_ip + '/rlfi.php'

    params = {'language': 'message.txt', 'action': 'go'}

    expected = 'Try to climb higher Spidy'

    assert not http.has_lfi(vulnerable_url, expected, params=params,
                            cookies=bwapp_cookie)
    assert not http.has_lfi(NONEXISTANT_SERVICE, expected, params=params,
                            cookies=bwapp_cookie)
    assert not http.has_lfi(BAD_FORMAT_SERVICE, expected, params=params,
                            cookies=bwapp_cookie)


@pytest.mark.parametrize('get_mock_ip', ['bwapp'], indirect=True)
def test_a8_csrf_close(get_mock_ip):
    """App vulnerable a Cross-Site Request Forgery?."""
    bwapp_cookie = get_bwapp_cookies(get_mock_ip)
    bwapp_cookie['security_level'] = '2'

    vulnerable_url = 'http://' + get_mock_ip + '/csrf_1.php'

    params = {'password_new': 'bug', 'password_conf': 'bug',
              'action': 'change'}

    expected = 'Current password'

    assert http.has_csrf(vulnerable_url, expected, params=params,
                         cookies=bwapp_cookie)
    assert not http.has_csrf(NONEXISTANT_SERVICE, expected, params=params,
                             cookies=bwapp_cookie)
    assert not http.has_csrf(BAD_FORMAT_SERVICE, expected, params=params,
                             cookies=bwapp_cookie)


def test_has_multiple_text_close():
    """Test has_multiple_text."""
    assert not http.has_multiple_text(f'{BASE_URL}/pragma/fail', regex_list=[
            'asdf',
            'qwer',
        ])
    assert not http.has_multiple_text(
        f'{MOCK_SERVICE}/http/error/500',
        regex_list=[
            'asdf',
            'qwer',
        ])


def test_access_control_allow_origin_close():
    """Header Access-Control-Allow-Origin establecido?."""
    assert http.is_header_access_control_allow_origin_missing(
        f'{BASE_URL}/access_control_allow_origin/ok/1', headers={}).is_closed()
    assert http.is_header_access_control_allow_origin_missing(
        f'{NONEXISTANT_SERVICE}/access_control_allow_origin/ok/1').is_unknown()
    assert http.is_header_access_control_allow_origin_missing(
        f'{BAD_FORMAT_SERVICE}/access_control_allow_origin/ok/1').is_unknown()
    assert http.is_header_access_control_allow_origin_missing(
        f'{BASE_URL}/access_control_allow_origin/ok/2', headers={}).is_closed()
    assert http.is_header_access_control_allow_origin_missing(
        f'{NONEXISTANT_SERVICE}/access_control_allow_origin/ok/2').is_unknown()
    assert http.is_header_access_control_allow_origin_missing(
        f'{BAD_FORMAT_SERVICE}/access_control_allow_origin/ok/2').is_unknown()


def test_cache_control_close():
    """Header Cache-Control establecido?."""
    assert http.is_header_cache_control_missing(
        '%s/cache_control/ok' % (BASE_URL)).is_closed()
    assert http.is_header_cache_control_missing(
        '%s/cache_control/ok' % (NONEXISTANT_SERVICE)).is_unknown()
    assert http.is_header_cache_control_missing(
        '%s/cache_control/ok' % (BAD_FORMAT_SERVICE)).is_unknown()


def test_pragma_close():
    """Check Pragma header."""
    assert http.is_header_pragma_missing(
        '%s/pragma/ok' % (BASE_URL)).is_closed()
    assert http.is_header_pragma_missing(
        '%s/pragma/ok' % (NONEXISTANT_SERVICE)).is_unknown()
    assert http.is_header_pragma_missing(
        '%s/pragma/ok' % (BAD_FORMAT_SERVICE)).is_unknown()


def test_hsts_close():
    """Header Strict-Transport-Security establecido?."""
    assert http.is_header_hsts_missing(f'{BASE_URL}/hsts/ok/1').is_closed()
    assert http.is_header_hsts_missing(f'{BASE_URL}/hsts/ok/2').is_closed()
    assert http.is_header_hsts_missing(
        f'{NONEXISTANT_SERVICE}/hsts/ok/1').is_unknown()
    assert http.is_header_hsts_missing(
        f'{NONEXISTANT_SERVICE}/hsts/ok/2').is_unknown()
    assert http.is_header_hsts_missing(
        f'{BAD_FORMAT_SERVICE}/hsts/ok/1').is_unknown()
    assert http.is_header_hsts_missing(
        f'{BAD_FORMAT_SERVICE}/hsts/ok/2').is_unknown()


def test_basic_close():
    """Auth BASIC no habilitado?."""
    assert http.is_basic_auth_enabled(f'{BASE_URL}/basic/ok').is_closed()
    assert http.is_basic_auth_enabled(
        f'{NONEXISTANT_SERVICE}/basic/ok').is_unknown()
    assert http.is_basic_auth_enabled(
        f'{BAD_FORMAT_SERVICE}/basic/ok').is_unknown()

    # this URL does not exist, but HTTPS is not vulnerable
    # it's just for testing purposes
    assert not http.is_basic_auth_enabled(f'https://localhost:5000/basic/ok')


def test_put_ok():
    """HTTP PUT ok."""
    assert not http.has_not_text('%s/put_ok' % (MOCK_SERVICE),
                                 'Method PUT Allowed', method='PUT')
    assert not http.has_not_text('%s/put_ok' % (NONEXISTANT_SERVICE),
                                 'Method PUT Allowed', method='PUT')
    assert not http.has_not_text('%s/put_ok' % (BAD_FORMAT_SERVICE),
                                 'Method PUT Allowed', method='PUT')


def test_delete_ok():
    """HTTP DELETE ok."""
    assert not http.has_not_text('%s/delete_ok' % (MOCK_SERVICE),
                                 'Method DELETE Allowed', method='DELETE')
    assert not http.has_not_text('%s/delete_ok' % (NONEXISTANT_SERVICE),
                                 'Method DELETE Allowed', method='DELETE')
    assert not http.has_not_text('%s/delete_ok' % (BAD_FORMAT_SERVICE),
                                 'Method DELETE Allowed', method='DELETE')


def test_put_close():
    """HTTP PUT Not Allowed."""
    assert not http.has_put_method(f'{BASE_URL}/put_close/1')
    assert not http.has_put_method(f'{NONEXISTANT_SERVICE}/put_close/1')
    assert not http.has_put_method(f'{BAD_FORMAT_SERVICE}/put_close/1')
    assert not http.has_put_method(f'{BASE_URL}/put_close/2')
    assert not http.has_put_method(f'{NONEXISTANT_SERVICE}/put_close/2')
    assert not http.has_put_method(f'{BAD_FORMAT_SERVICE}/put_close/2')


def test_trace_close():
    """HTTP TRACE Not Allowed."""
    assert not http.has_trace_method('%s/trace_close' % (BASE_URL))
    assert not http.has_trace_method('%s/trace_close' % (NONEXISTANT_SERVICE))
    assert not http.has_trace_method('%s/trace_close' % (BAD_FORMAT_SERVICE))


def test_delete_close():
    """HTTP DELETE Not Allowed."""
    assert not http.has_delete_method('%s/delete_close' % (BASE_URL))
    assert not http.has_delete_method('%s/delete_close' %
                                      (NONEXISTANT_SERVICE))
    assert not http.has_delete_method('%s/delete_close' %
                                      (BAD_FORMAT_SERVICE))


def test_notfound_string_close():
    """Expected string not found?."""
    url = '%s/notfound' % (BASE_URL)
    expected = 'Expected string'
    assert not http.has_text(url, expected)
    assert not http.has_text(NONEXISTANT_SERVICE, expected)
    assert not http.has_text(BAD_FORMAT_SERVICE, expected)


def test_found_string_close():
    """Expected string not found?."""
    url = '%s/expected' % (BASE_URL)
    expected = 'Expected string'
    assert not http.has_not_text(url, expected)
    assert not http.has_not_text(NONEXISTANT_SERVICE, expected)
    assert not http.has_not_text(BAD_FORMAT_SERVICE, expected)


def test_userenum_post_close():
    """Enumeracion de usuarios posible?."""
    data = 'username=pepe&password=grillo'
    data_bad = 'a=pepe&b=grillo'
    assert not http.has_user_enumeration(
        '%s/userenum_post/ok' % (MOCK_SERVICE),
        'username', data=data)
    assert not http.has_user_enumeration(
        '%s/userenum_post/ok' % (MOCK_SERVICE),
        'username', data=data_bad)
    assert not http.has_user_enumeration(
        '%s/userenum_post/ok' % (MOCK_SERVICE),
        'username')
    assert not http.has_user_enumeration(
        '%s/userenum_post/ok' % (NONEXISTANT_SERVICE),
        'username', data=data)
    assert not http.has_user_enumeration(
        '%s/userenum_post/ok' % (BAD_FORMAT_SERVICE),
        'username', data=data)


def test_userenum_post_json_close():
    """Enumeracion de usuarios posible?."""
    data = {'username': 'pepe',
            'password': 'grillo'}
    assert not http.has_user_enumeration(
        '%s/userenum_post/json/ok' % (MOCK_SERVICE),
        'username', json=data)
    assert not http.has_user_enumeration(
        '%s/userenum_post/json/ok' % (NONEXISTANT_SERVICE),
        'username', json=data)
    assert not http.has_user_enumeration(
        '%s/userenum_post/json/ok' % (BAD_FORMAT_SERVICE),
        'username', json=data)


def test_userenum_get_close():
    """Enumeracion de usuarios posible?."""
    data = 'username=pepe&password=grillo'
    assert not http.has_user_enumeration(
        '%s/userenum_get/ok' % (MOCK_SERVICE),
        'username', params=data)
    assert not http.has_user_enumeration(
        '%s/userenum_get/ok' % (NONEXISTANT_SERVICE),
        'username', params=data)
    assert not http.has_user_enumeration(
        '%s/userenum_get/ok' % (BAD_FORMAT_SERVICE),
        'username', params=data)
    assert not http.has_user_enumeration(
        NONEXISTANT_SERVICE, 'username', params=data)
    assert not http.has_user_enumeration(
        BAD_FORMAT_SERVICE, 'username', params=data)


def test_bruteforce_close():
    """Bruteforce posible?."""
    data = 'username=pepe&password=grillo'
    assert not http.can_brute_force(
        '%s/bruteforce/ok' % (MOCK_SERVICE),
        'admin',
        'username',
        'password',
        user_list=['root', 'admin'],
        pass_list=['pass', 'password'],
        data=data)
    assert not http.can_brute_force(
        '%s/bruteforce/ok' % (MOCK_SERVICE),
        'admin',
        'username',
        'password',
        user_list=['root', 'admin'],
        pass_list=['pass', 'password'])
    assert not http.can_brute_force(
        '%s/bruteforce/ok' % (NONEXISTANT_SERVICE),
        'admin',
        'username',
        'password',
        user_list=['root', 'admin'],
        pass_list=['pass', 'password'],
        data=data)
    assert not http.can_brute_force(
        '%s/bruteforce/ok' % (BAD_FORMAT_SERVICE),
        'admin',
        'username',
        'password',
        user_list=['root', 'admin'],
        pass_list=['pass', 'password'],
        data=data)


def test_responsetime_close():
    """Tiempo de respuesta aceptable?."""
    assert not http.is_response_delayed(
        '%s/responsetime/ok' % (MOCK_SERVICE))
    assert not http.is_response_delayed(
        '%s/responsetime/ok' % (NONEXISTANT_SERVICE))
    assert not http.is_response_delayed(
        '%s/responsetime/ok' % (BAD_FORMAT_SERVICE))


def test_dirlisting_close():
    """Dirlisting habilitado?."""
    assert not http.has_dirlisting(
        '%s/dirlisting/ok' % (MOCK_SERVICE))
    assert not http.has_dirlisting(
        '%s/dirlisting/ok' % (NONEXISTANT_SERVICE))
    assert not http.has_dirlisting(
        '%s/dirlisting/ok' % (BAD_FORMAT_SERVICE))


def test_http_response_close():
    """Respuesta 403 FORBIDDEN?."""
    assert not http.is_resource_accessible(
        '%s/response/ok' % (MOCK_SERVICE))
    assert not http.is_resource_accessible(
        '%s/response/ok' % (NONEXISTANT_SERVICE))
    assert not http.is_resource_accessible(
        '%s/response/ok' % (BAD_FORMAT_SERVICE))


def test_is_header_x_asp_net_version_present_close():
    """Header X-AspNet-Version establecido?."""
    assert http.is_header_x_asp_net_version_present(
        '%s/x_aspnet_version/ok' % (BASE_URL)).is_closed()
    assert http.is_header_x_asp_net_version_present(
        '%s/x_aspnet_version/ok' % (NONEXISTANT_SERVICE)).is_unknown()
    assert http.is_header_x_asp_net_version_present(
        '%s/x_aspnet_version/ok' % (BAD_FORMAT_SERVICE)).is_unknown()


def test_is_header_x_powered_by_present_close():
    """Check X-Powered-By header."""
    assert http.is_header_x_powered_by_present(
        '%s/x_powered_by/ok' % (BASE_URL)).is_closed()
    assert http.is_header_x_powered_by_present(
        '%s/x_powered_by/ok' % (NONEXISTANT_SERVICE)).is_unknown()
    assert http.is_header_x_powered_by_present(
        '%s/x_powered_by/ok' % (BAD_FORMAT_SERVICE)).is_unknown()


def test_content_options_close():
    """Check X-Content-Type-Options header."""
    assert http.is_header_x_content_type_options_missing(
        '%s/content_type/ok' % (BASE_URL)).is_closed()
    assert http.is_header_x_content_type_options_missing(
        '%s/content_type/ok' % (NONEXISTANT_SERVICE)).is_unknown()
    assert http.is_header_x_content_type_options_missing(
        '%s/content_type/ok' % (BAD_FORMAT_SERVICE)).is_unknown()


def test_frame_options_close():
    """Check X-Frame-Options header."""
    assert http.is_header_x_frame_options_missing(
        '%s/frame_options/ok' % (BASE_URL)).is_closed()
    assert http.is_header_x_frame_options_missing(
        '%s/frame_options/ok' % (NONEXISTANT_SERVICE)).is_unknown()
    assert http.is_header_x_frame_options_missing(
        '%s/frame_options/ok' % (BAD_FORMAT_SERVICE)).is_unknown()


def test_server_close():
    """Check Server header."""
    assert http.is_header_server_present(BAD_FORMAT_SERVICE).is_unknown()
    assert http.is_header_server_present(NONEXISTANT_SERVICE).is_unknown()


def test_expires_close():
    """Check Expires header."""
    assert http.is_header_expires_missing(NO_HEADERS).is_closed()
    assert http.is_header_expires_missing(
        '%s/expires/ok' % (BASE_URL)).is_closed()
    assert http.is_header_expires_missing(
        '%s/expires/ok' % (NONEXISTANT_SERVICE)).is_unknown()
    assert http.is_header_expires_missing(
        '%s/expires/ok' % (BAD_FORMAT_SERVICE)).is_unknown()


def test_content_type_close():
    """Check Content-Type header."""
    assert http.is_header_content_type_missing(
        '%s/content_type/ok' % (BASE_URL)).is_closed()
    assert http.is_header_content_type_missing(
        '%s/content_type/ok' % (NONEXISTANT_SERVICE)).is_unknown()
    assert http.is_header_content_type_missing(
        '%s/content_type/ok' % (BAD_FORMAT_SERVICE)).is_unknown()


def test_content_security_policy_missing_close():
    """Check Content-Security-Policy header."""
    assert http.is_header_content_security_policy_missing(
        '%s/content_security_policy/ok' % (BASE_URL)).is_closed()
    assert http.is_header_content_security_policy_missing(
        '%s/content_security_policy/ok' % (NONEXISTANT_SERVICE)).is_unknown()
    assert http.is_header_content_security_policy_missing(
        '%s/content_security_policy/ok' % (BAD_FORMAT_SERVICE)).is_unknown()


def test_is_version_visible_close():
    """Server header contains version?."""
    assert not http.is_version_visible('%s/version/ok' % (BASE_URL))
    assert not http.is_version_visible('%s/version/ok' % (NONEXISTANT_SERVICE))
    assert not http.is_version_visible('%s/version/ok' % (BAD_FORMAT_SERVICE))


def test_is_header_x_xxs_protection_missing_close():
    """Header x-xss-protection establecido?."""
    assert http.is_header_x_xxs_protection_missing(
        '%s/xxs_protection/ok' % (BASE_URL)).is_closed()
    assert http.is_header_x_xxs_protection_missing(
        '%s/xxs_protection/ok' % (NONEXISTANT_SERVICE)).is_unknown()
    assert http.is_header_x_xxs_protection_missing(
        '%s/xxs_protection/ok' % (BAD_FORMAT_SERVICE)).is_unknown()


def test_is_header_perm_cross_dom_pol_missing_close():
    """Header cross-domain-policy establecido?."""
    assert http.is_header_perm_cross_dom_pol_missing(
        '%s/perm_cross_dom_pol/ok' % (BASE_URL)).is_closed()
    assert http.is_header_perm_cross_dom_pol_missing(
        '%s/perm_cross_dom_pol/ok' % (NONEXISTANT_SERVICE)).is_unknown()
    assert http.is_header_perm_cross_dom_pol_missing(
        '%s/perm_cross_dom_pol/ok' % (BAD_FORMAT_SERVICE)).is_unknown()


def test_has_clear_viewstate_close():
    """Esta el ViewState cifrado?."""
    assert not http.has_clear_viewstate(
        '%s/http/viewstate/encrypted/ok' % (MOCK_SERVICE))
    assert not http.has_clear_viewstate(
        '%s/http/viewstate/encrypted/not_found' % (MOCK_SERVICE))
    assert not http.has_clear_viewstate(
        '%s/http/viewstate/encrypted/not_found' % (NONEXISTANT_SERVICE))
    assert not http.has_clear_viewstate(
        '%s/http/viewstate/encrypted/not_found' % (BAD_FORMAT_SERVICE))


def test_is_date_unsyncd_close():
    """Hora desincronizada?."""
    assert not http.is_date_unsyncd(f'{BASE_URL}/date/ok')
    assert not http.is_date_unsyncd(BAD_FORMAT_SERVICE)
    assert not http.is_date_unsyncd(NONEXISTANT_SERVICE)


def test_is_not_https_required_close():
    """El servidor no requiere usar HTTPS?."""
    assert not http.is_not_https_required(NONEXISTANT_SERVICE)
    assert not http.is_not_https_required(BAD_FORMAT_SERVICE)
    assert not http.is_not_https_required('https://127.0.0.1')


def test_host_injection_close():
    """Server vulnerable to Host header injection?."""
    assert not http.has_host_header_injection(
        '%s/host_injection_ok' % (BASE_URL))
    assert not http.has_host_header_injection(
        '%s/host_injection_ok' % (BASE_URL),
        headers={'Host': 'fluidattacks.com'})
    assert not http.has_host_header_injection(
        '%s/host_not_found' % (BASE_URL))
    assert not http.has_host_header_injection(
        '%s/host_injection_ok' % (NONEXISTANT_SERVICE))
    assert not http.has_host_header_injection(
        '%s/host_injection_ok' % (BAD_FORMAT_SERVICE))


def test_mixed_content_close():
    """Resource has mixed content?."""
    assert not http.has_mixed_content(BASE_URL)
    assert not http.has_mixed_content(NONEXISTANT_SERVICE)
    assert not http.has_mixed_content(BAD_FORMAT_SERVICE)
    assert not http.has_mixed_content('https://google.com')


def test_has_reverse_tabnabbing_close():
    """Check if site has reverse tabnabbing."""
    assert not http.has_reverse_tabnabbing(BASE_URL)
    assert not http.has_reverse_tabnabbing(NONEXISTANT_SERVICE)
    assert not http.has_reverse_tabnabbing(BAD_FORMAT_SERVICE)
    assert not http.has_reverse_tabnabbing(
        f'{MOCK_SERVICE}/http/reverse_tabnabbing/ok/1')


def test_insecure_upload_close():
    """Check insecure upload."""
    assert not http.has_insecure_upload(
        f'{MOCK_SERVICE}/upload_secure',
        'uploaded_file OK',
        'file',
        'test/static/example/test_open.py')
    assert not http.has_insecure_upload(
        f'{BASE_URL}/host_not_found',
        'uploaded_file OK',
        'file',
        'test/static/example/test_open.py')
    assert not http.has_insecure_upload(
        f'{NONEXISTANT_SERVICE}/upload_secure',
        'uploaded_file OK',
        'file',
        'test/static/example/test_open.py')
    assert not http.has_insecure_upload(
        f'{BAD_FORMAT_SERVICE}/upload_secure',
        'uploaded_file OK',
        'file',
        'test/static/example/test_open.py')
