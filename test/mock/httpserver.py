# -*- coding: utf-8 -*-

u"""Servidor HTTP basado en Flask para exponer los mock HTTP.

Este modulo necesita un serio refactoring para reutilizar una logica
mas simple y menos repetitiva donde puede operar sobre una estructura
de datos que defina por cada header:

1. Nombre del header en el protocolo,
2. Valor satisfactorio del header,
3. Valor no satisfactorio del header,
4. URL base (opcional puede ser generada por la función a partir de 1,2 y 3)
5. Cuerpo de respuesta (opcional, ver razon de 4).

El metodo opera sobre esta estructura y a partir de los datos anteriores
y un formato definido de url:

http://xxx/header/ok -> responde con 2
http://xxx/header/fail -> responde con 3

Genera la respuesta correspondiente, tanto en el body, como en los headers

El refactoring sera adecuado cuando se añadan a la estructura de datos
nuevos headers y funcione para más casos de prueba.
"""

# standard imports
import os
import time
import random
import datetime

# 3rd party imports
from flask import Flask
from flask import redirect
from flask import request
from flask import Response
from flask import url_for


# local imports
# none

UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = {'txt', 'pdf'}
APP = Flask(__name__, static_folder='static', static_url_path='/static')

APP.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    """Filter allowed files."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@APP.route('/upload_secure', methods=['POST'])
def upload_file_secure():
    """Create upload mock."""
    if 'file' not in request.files:
        return 'No file part'
    my_file = request.files['file']
    if my_file.filename == '':
        return 'No selected file'
    if my_file and allowed_file(my_file.filename):
        my_file.save(os.path.join(APP.config['UPLOAD_FOLDER'],
                                  my_file.filename))
        return 'uploaded_file OK'
    return 'upload_file failed'


@APP.route('/upload_insecure', methods=['POST'])
def upload_file_insecure():
    """Create upload mock."""
    if 'file' not in request.files:
        return 'No file part'
    my_file = request.files['file']
    if my_file.filename == '':
        return 'No selected file'
    if my_file:
        my_file.save(os.path.join(APP.config['UPLOAD_FOLDER'],
                                  my_file.filename))
        return 'uploaded_file OK'
    return 'upload_file failed'


@APP.route('/')
def home():
    """Respuesta a directorio raiz."""
    return 'Mock HTTP Server'


@APP.route('/noheaders')
def noheaders():
    """Response with no headers."""
    resp = Response(response='Headers? who needs them?')
    resp.headers = {}
    return resp


@APP.route('/responsetime/ok')
def responsetime_ok():
    """Tiempo de respuesta OK."""
    return 'OK'


@APP.route('/responsetime/fail')
def responsetime_fail():
    """Tiempo de respuesta fail."""
    time.sleep(2)
    return 'FAIL'


@APP.route('/dirlisting/ok')
def dirlisting_ok():
    """Dirlisting deshabilitado."""
    return 'OK'


@APP.route('/dirlisting/fail')
def dirlisting_fail():
    """Dirlisting habilitado."""
    return 'Index of'


@APP.route('/response/fail')
def response_fail():
    """Respuesta 201 CREATED."""
    resp = Response()
    resp.status_code = 201
    return resp


@APP.route('/response/ok')
def response_ok():
    """Respuesta 403 FORBIDDEN."""
    resp = Response()
    resp.status_code = 403
    return resp


@APP.route('/userenum_post/fail', methods=['POST'])
def user_enumeration_post_fail():
    """Form vuln a user enumeration."""
    if request.values['username'] == 'admin':
        return 'Login incorrect'
    return 'User not found'


@APP.route('/userenum_post/ok', methods=['POST'])
def user_enumeration_post_ok():
    """Form segura a user enumeration."""
    return 'Login incorrect'


@APP.route('/userenum_post/json/fail', methods=['POST'])
def user_enumeration_post_json_fail():
    """Form vuln a user enumeration."""
    if request.get_json()['username'] == 'admin':
        return 'Login incorrect'
    return 'User not found'


@APP.route('/userenum_post/nested_json/fail', methods=['POST'])
def user_enumeration_post_nested_json_fail():
    """Form vuln a user enumeration."""
    if request.get_json()['login']['username'] == 'admin':
        return 'Login incorrect'
    return 'User not found'


@APP.route('/userenum_post/json/ok', methods=['POST'])
def user_enumeration_post_json_ok():
    """Form segura a user enumeration."""
    return 'Login incorrect'


@APP.route('/userenum_get/fail', methods=['GET'])
def user_enumeration_get_fail():
    """Form vuln a user enumeration."""
    if request.values['username'] == 'admin':
        return 'Login incorrect'
    return 'User not found'


@APP.route('/userenum_get/ok', methods=['GET'])
def user_enumeration_get_ok():
    """Form segura a user enumeration."""
    return 'Login incorrect'


@APP.route('/bruteforce/fail_get', methods=['GET'])
def brute_force_get_fail():
    """Form con brute forcing."""
    if request.values['username'] == 'admin' and \
       request.values['password'] == 'password':
        return 'You are admin now'
    return 'Login incorrect'


@APP.route('/bruteforce/fail_post', methods=['POST'])
def brute_force_post_fail():
    """Form con brute forcing."""
    if request.values['username'] == 'admin' and \
       request.values['password'] == 'password':
        return 'You are admin now'
    return 'Login incorrect'


@APP.route('/bruteforce/fail_json', methods=['POST'])
def brute_force_json_fail():
    """Form con brute forcing."""
    if request.get_json()['username'] == 'admin' and \
       request.get_json()['password'] == 'password':
        return 'You are admin now'
    return 'Login incorrect'


@APP.route('/bruteforce/ok', methods=['POST'])
def brute_force_ok():
    """Form sin brute forcing."""
    if request.values['username'] == 'admin' and \
       request.values['password'] == 'password':
        return 'You need a second factor'
    return 'Login incorrect'


@APP.route('/http/headers/access_control_allow_origin/ok/1')
def access_control_allow_origin_ok_1():
    """Header AC Allow Origin bien establecido."""
    resp = Response('Access-Control-Allow-Origin OK')
    resp.headers['Access-Control-Allow-Origin'] = 'https://fluid.la'
    return resp


@APP.route('/http/headers/access_control_allow_origin/ok/2')
def access_control_allow_origin_ok_2():
    """Header AC Allow Origin bien establecido."""
    resp = Response('Access-Control-Allow-Origin OK')
    return resp


@APP.route('/http/headers/access_control_allow_origin/fail')
def access_control_allow_origin_fail():
    """Header AC Allow Origin mal establecido."""
    resp = Response('Access-Control-Allow-Origin FAIL')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@APP.route('/http/headers/cache_control/ok')
def cache_control_ok():
    """Header para Control de Cache bien establecido."""
    resp = Response('Cache-Control OK')
    resp.headers[
        'Cache-Control'] = ('no-cache, no-store, must-revalidate')
    return resp


@APP.route('/http/headers/pragma/fail')
def pragma_fail():
    """Header para Control de Cache bien establecido."""
    resp = Response('Pragma FAIL')
    resp.headers['Pragma'] = ('cache')
    return resp


@APP.route('/http/headers/pragma/ok')
def pragma_ok():
    """Header para Control de Cache bien establecido."""
    resp = Response('Pragma OK')
    resp.headers['Pragma'] = ('no-cache')
    return resp


@APP.route('/http/headers/cache_control/fail')
def cache_control_fail():
    """Header para Control de Cache mal establecido."""
    resp = Response('Cache-Control FAIL')
    resp.headers['Cache-Control'] = 'Fail'
    return resp


@APP.route('/http/headers/content_options/ok')
def content_options_ok():
    """Run X-Content-Type-Options mock."""
    resp = Response('content-security-policy OK')
    resp.headers[
        'X-Content-Type-Options'] = "nosniff"
    return resp


@APP.route('/http/headers/content_options/fail')
def content_options_fail():
    """Run X-Content-Type-Options mock."""
    resp = Response('Content-Security-Policy FAIL')
    resp.headers['X-Content-Type-Options'] = 'Fail'
    return resp


@APP.route('/rest/content_options/ok')
def rest_content_options_ok():
    """Run X-Content-Type-Options mock."""
    resp = Response('content-security-policy OK')
    resp.headers[
        'X-Content-Type-Options'] = "nosniff"
    return resp


@APP.route('/rest/content_options/fail')
def rest_content_options_fail():
    """Run X-Content-Type-Options mock."""
    resp = Response('Content-Security-Policy FAIL')
    resp.headers['X-Content-Type-Options'] = 'Fail'
    return resp


@APP.route('/http/headers/frame_options/ok')
def frame_options_ok():
    """Run X-Frame-Options mock."""
    resp = Response('content-security-policy OK')
    resp.headers[
        'X-Frame-Options'] = "sameorigin"
    return resp


@APP.route('/http/headers/frame_options/fail')
def frame_options_fail():
    """Run X-Frame-Options mock."""
    resp = Response('Content-Security-Policy FAIL')
    resp.headers['X-Frame-Options'] = 'Fail'
    return resp


@APP.route('/rest/frame_options/ok')
def rest_frame_options_ok():
    """Run X-Frame-Options mock."""
    resp = Response('content-security-policy OK')
    resp.headers[
        'X-Frame-Options'] = "deny"
    return resp


@APP.route('/rest/frame_options/fail')
def rest_frame_options_fail():
    """Run X-Frame-Options mock."""
    resp = Response('Content-Security-Policy FAIL')
    resp.headers['X-Frame-Options'] = 'fail'
    return resp


@APP.route('/http/headers/content_security_policy/ok')
def content_security_policy_ok():
    """Header para politica de contenido bien establecida."""
    resp = Response('content-security-policy OK')
    resp.headers[
        'Content-Security-Policy'] = "default-src 'self' *.trusted.com"
    return resp


@APP.route('/http/headers/content_security_policy/fail')
def content_security_policy_fail():
    """Header para politica de contenido mal establecida."""
    resp = Response('Content-Security-Policy FAIL')
    resp.headers['Content-Security-Policy'] = 'Fail'
    return resp


@APP.route('/http/headers/content_type/ok')
def content_type_ok():
    """Header que define bien el tipo de contenido."""
    resp = Response('Content-Type OK')
    resp.headers['Content-Type'] = 'application/json; charset=utf-8'
    resp.headers['X-Content-Type-Options'] = 'nosniff'
    return resp


@APP.route('/http/headers/content_type/fail')
def content_type_fail():
    """Header que define mal el tipo de contenido."""
    resp = Response('Content-Type FAIL')
    resp.headers['Content-Type'] = 'application/json'
    return resp


@APP.route('/rest/content_type/ok')
def rest_content_type_ok():
    """Header que define bien el tipo de contenido."""
    resp = Response('Content-Type OK')
    resp.headers['Content-Type'] = 'application/json; charset=utf-8'
    resp.headers['X-Content-Type-Options'] = 'nosniff'
    return resp


@APP.route('/rest/content_type/fail')
def rest_content_type_fail():
    """Header que define mal el tipo de contenido."""
    resp = Response('Content-Type FAIL')
    resp.headers['Content-Type'] = 'application/json'
    return resp


@APP.route('/http/headers/expires/ok')
def expires_ok():
    u"""Header que define bien la expiración de la página en cache."""
    resp = Response('Expires OK')
    resp.headers['Expires'] = '0'
    return resp


@APP.route('/http/headers/expires/fail')
def expires_fail():
    u"""Header que define mal la expiración de la página en cache."""
    resp = Response('Expires FAIL')
    resp.headers['Expires'] = 'Fail'
    return resp


@APP.route('/http/headers/hsts/ok/1')
def hsts_ok_1():
    """Header que define bien la implementacion de HSTS."""
    resp = Response('Expires OK')
    resp.headers['Strict-Transport-Security'] = 'max-age= 31536000; \
        includeSubDomains; preload'
    return resp


@APP.route('/http/headers/hsts/ok/2')
def hsts_ok_2():
    """Header que define bien la implementacion de HSTS."""
    resp = Response('Expires OK')
    resp.headers['Strict-Transport-Security'] = 'max-age= "31536000"; \
        includeSubDomains; preload'
    return resp


@APP.route('/http/headers/hsts/fail/1')
def hsts_fail_1():
    """Header que define mal implementacion de HSTS."""
    resp = Response('Expires FAIL')
    return resp


@APP.route('/http/headers/hsts/fail/2')
def hsts_fail_2():
    """Header que define mal implementacion de HSTS."""
    resp = Response('Expires FAIL')
    resp.headers['Strict-Transport-Security'] = 'max-age=31536000"; \
        includeSubDomains; preload'
    return resp


@APP.route('/http/headers/hsts/fail/3')
def hsts_fail_3():
    """Header que define mal implementacion de HSTS."""
    resp = Response('Expires FAIL')
    resp.headers['Strict-Transport-Security'] = 'max-age=86400; \
        includeSubDomains; preload'
    return resp


@APP.route('/http/headers/server/fail')
def server_fail():
    """Header Server inseguro."""
    resp = Response('Server header FAIL')
    resp.headers['Strict-Transport-Security'] = 'Fail'
    resp.headers['Cosa'] = 'Cosa'
    resp.headers['Server'] = 'Apache'
    return resp


@APP.route('/http/headers/version/ok')
def version_ok():
    """Header Server seguro."""
    resp = Response('Server header OK')
    resp.headers['Server'] = 'Apache'
    return resp


@APP.route('/http/headers/version/fail')
def version_fail():
    """Header Server inseguro."""
    resp = Response('Server header FAIL')
    resp.headers['Strict-Transport-Security'] = 'Fail'
    resp.headers['Cosa'] = 'Cosa'
    resp.headers['Server'] = 'Apache/2.4.10 (Debian) OpenSSL/1.0.1t'
    return resp


@APP.route('/http/headers/basic/ok')
def basic_ok():
    """Header que define bien la implementacion de HTTP Auth."""
    resp = Response('Basic Auth OK')
    resp.headers['WWW-Authenticate'] = 'NTLM'
    return resp


@APP.route('/http/headers/basic/fail')
def basic_fail():
    """Header que define mal implementacion de HTTP Auth."""
    resp = Response('Basic Auth FAIL')
    resp.headers['WWW-Authenticate'] = 'Basic'
    return resp


@APP.route('/http/headers/put_close/1', methods=['OPTIONS'])
def put_close_1():
    """Metodo PUT deshabilitado."""
    resp = Response("Method PUT not Allowed")
    resp.headers['allow'] = 'HEAD, OPTIONS, GET, POST, OPTIONS'
    return resp

@APP.route('/http/headers/put_close/2', methods=['OPTIONS'])
def put_close_2():
    """Metodo PUT deshabilitado."""
    resp = Response("Method PUT not Allowed")
    return resp


@APP.route('/http/headers/put_open', methods=['OPTIONS'])
def put_open():
    """Metodo PUT habilitado."""
    resp = Response("Method PUT Allowed")
    resp.headers['allow'] = 'PUT'
    return resp


@APP.route('/put_ok', methods=['PUT'])
def put_ok():
    """Metodo PUT."""
    resp = Response("Method PUT Allowed")
    return resp


@APP.route('/delete_ok', methods=['DELETE'])
def delete_ok():
    """Metodo DELETE."""
    resp = Response("Method DELETE Allowed")
    return resp


@APP.route('/http/headers/trace_close', methods=['OPTIONS'])
def trace_close():
    """Metodo TRACE deshabilitado."""
    resp = Response("Method TRACE not Allowed")
    resp.headers['allow'] = 'HEAD, OPTIONS, GET, POST, OPTIONS'
    return resp


@APP.route('/http/headers/trace_open', methods=['OPTIONS'])
def trace_open():
    """Metodo TRACE habilitado."""
    resp = Response("Method TRACE Allowed")
    resp.headers['allow'] = 'TRACE'
    return resp


@APP.route('/http/headers/delete_close', methods=['OPTIONS'])
def delete_close():
    """Metodo DELETE deshabilitado."""
    resp = Response("Method DELETE not Allowed")
    resp.headers['allow'] = 'HEAD, OPTIONS, GET, POST, OPTIONS'
    return resp


@APP.route('/http/headers/delete_open', methods=['OPTIONS'])
def delete_open():
    """Metodo DELETE habilitado."""
    resp = Response("Method DELETE Allowed")
    resp.headers['allow'] = 'DELETE'
    return resp


@APP.route('/http/headers/expected')
def expected_string():
    """Cadena Esperada."""
    return "Expected string"


@APP.route('/http/headers/notfound')
def notfound_string():
    """Cadena no encontrada."""
    return "Randomstring"


@APP.route('/http/headers/session_fixation_open')
def session_fixation_open():
    """Robo de sesion abierto."""
    return redirect(url_for('session_fixated_vuln', sessionid=12345678),
                    code=302)


@APP.route('/http/headers/sessionfixated_url')
def session_fixated_vuln():
    """Vulnerable a robo de sesion."""
    resp = Response("Login successful")
    return resp


@APP.route('/http/headers/session_fixation_close')
def session_fixation_close():
    """Robo de sesion Cerrado."""
    return redirect(url_for('session_fixated_not_vuln', sessionid=12345678),
                    code=302)


@APP.route('/http/headers/session_not_fixated_url')
def session_fixated_not_vuln():
    """No vulnerable a robo de session."""
    if request.cookies.get('login_ok') is True:
        resp = Response('Login successful')
    else:
        resp = Response('Login required')
    return resp


@APP.route('/http/cookies/secure/fail')
def secure_fail():
    """Cookie sin atributo de seguridad secure."""
    resp = Response('Login successful')
    resp.set_cookie('JSESSID', 'World', secure=False, httponly=True)
    return resp


@APP.route('/http/cookies/secure/ok')
def secure_ok():
    """Cookie con atributo de seguridad secure."""
    resp = Response('Login successful')
    resp.set_cookie('JSESSID', 'World', secure=True, httponly=True)
    return resp


@APP.route('/http/cookies/http_only/fail')
def http_only_fail():
    """Cookie sin atributo de seguridad http-only."""
    resp = Response('Login successful')
    resp.set_cookie('JSESSID', 'World', secure=True, httponly=False,
                    samesite='lax')
    return resp


@APP.route('/http/cookies/http_only/ok')
def http_only_ok():
    """Cookie con atributo de seguridad http-only."""
    resp = Response('Login successful')
    resp.set_cookie('JSESSID', 'World', secure=True, httponly=True,
                    samesite='strict')
    return resp


@APP.route('/http/headers/x_aspnet_version/ok')
def x_aspnet_version_ok():
    """Encabezado X-AspNet-Version no presente."""
    resp = Response('Login successful')
    return resp


@APP.route('/http/headers/x_aspnet_version/fail')
def x_aspnet_version_fail():
    """Encabezado X-AspNet-Version presente."""
    resp = Response('Login successful')
    resp.headers['X-AspNet-Version'] = '2.0.502727'
    return resp


@APP.route('/http/headers/x_powered_by/ok')
def x_powered_by_ok():
    """Encabezado X-Powered-By no presente."""
    resp = Response('Login successful')
    return resp


@APP.route('/http/headers/x_powered_by/fail')
def x_powered_by_fail():
    """Encabezado X-Powered-By presente."""
    resp = Response('Login successful')
    resp.headers['X-Powered-By'] = 'ASP.NET'
    return resp


@APP.route('/http/headers/xxs_protection/ok')
def xxs_protection_ok():
    """Encabezado X-XSS-Protection presente."""
    resp = Response('Login successful')
    resp.headers['X-XSS-Protection'] = '1; mode=block'
    return resp


@APP.route('/http/headers/xxs_protection/fail')
def xxs_protection_fail():
    """Encabezado X-XSS-Protection deshabilitado."""
    resp = Response('Login successful')
    resp.headers['X-XSS-Protection'] = '0'
    return resp


@APP.route('/http/headers/perm_cross_dom_pol/ok')
def perm_cross_dom_pol_ok():
    """Encabezado X-XSS-Protection presente."""
    resp = Response('Login successful')
    resp.headers['X-Permitted-Cross-Domain-Policies'] = 'none'
    return resp


@APP.route('/http/headers/perm_cross_dom_pol/fail')
def perm_cross_dom_pol_fail():
    """Encabezado X-XSS-Protection deshabilitado."""
    resp = Response('Login successful')
    resp.headers['X-Permitted-Cross-Domain-Policies'] = 'all'
    return resp


@APP.route('/http/viewstate/encrypted/ok')
def viewstate_encrypted_ok():
    """Set ViewState encrypted."""
    resp = Response('<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE"\
value="zbsXSMp8dJ5Pk8V0yeeEHHyIJyNFnYpw" />')
    return resp


@APP.route('/http/viewstate/encrypted/fail')
def viewstate_encrypted_fail():
    """Set ViewState unencrypted."""
    resp = Response('<input type="hidden" name="__VIEWSTATE"' +
                    'id="__VIEWSTATE" value="/wEPBQVhYmNkZQ9nAgE=" />')
    return resp


@APP.route('/http/viewstate/encrypted/not_found')
def viewstate_encrypted_notfound():
    """Set ViewState not found."""
    resp = Response('Login successful')
    return resp


@APP.route('/http/headers/date/ok')
def date_ok():
    """Date actualizada."""
    resp = Response()
    resp.headers['Date'] = \
        datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
    return resp


@APP.route('/http/headers/date/fail')
def date_fail():
    """Date desactualizada."""
    resp = Response()
    resp.headers['Date'] = 'Wed, 23 May 1970 00:00:00 GMT'
    return resp


@APP.route('/http/error/500')
def error_500():
    """Error 500."""
    resp = Response('Error')
    resp.status_code = 500
    return resp


@APP.route('/http/headers/host_injection_fail')
def host_injection_fail():
    """Vulnerable a Host injection."""
    resp = Response()
    resp.headers['Location'] = 'http://' + request.headers['Host']
    return resp


@APP.route('/http/headers/host_injection_ok')
def host_injection_ok():
    """Vulnerable a Host injection."""
    resp = Response()
    resp.headers['Location'] = 'http://legitsite.com'
    return resp


@APP.route('/http/reverse_tabnabbing/ok/1', methods=['GET'])
def http_reverse_tabnabbing_ok_1():
    """Response for ."""
    url: str = 'https://mathiasbynens.github.io/rel-noopener/malicious.html'
    return Response(f"""
        <html>
            <body>
                <li>
                    <a href="{url}" target="_blank" rel="noopener noreferrer">
                        Click me for a reverse tabnabbing
                    </a>
                </li>
            </body>
        </html>
        """)


@APP.route('/http/reverse_tabnabbing/fail/1', methods=['GET'])
def http_reverse_tabnabbing_fail_1():
    """Response for ."""
    url: str = 'https://mathiasbynens.github.io/rel-noopener/malicious.html'
    return Response(f"""
        <html>
            <body>
                <li>
                    <a href="{url}" target="_blank">
                        Click me for a reverse tabnabbing
                    </a>
                </li>
            </body>
        </html>
        """)


@APP.route('/http/reverse_tabnabbing/fail/2', methods=['GET'])
def http_reverse_tabnabbing_fail_2():
    """Response for ."""
    url: str = 'https://mathiasbynens.github.io/rel-noopener/malicious.html'
    return Response(f"""
        <html>
            <body>
                <li>
                    <a href="{url}" target="_blank" rel='noreferrer'>
                        Click me for a reverse tabnabbing
                    </a>
                </li>
            </body>
        </html>
        """)


@APP.route('/http/xsl/frame', methods=['GET'])
def http_xsl_frames():
    """Return an HTML with three frames."""
    return Response(f"""
        <html>
            <body>
                Account ID: {os.urandom(8).hex()} <br />
                Balance   : {random.randint(0, 1e6)}
            </body>
        </html>
        """)


@APP.route('/http/xsl/frames/<int:num>', methods=['GET'])
def http_xsl_frames_id(num: int):
    """Return an HTML with three frames."""
    new_line: str = '\n'
    iframe: str = '<iframe src="/http/xsl/frame"></iframe>'
    return Response(f"""
        <html>
            <body>
                {new_line.join(iframe for _ in range(num))}
            </body>
        </html>
        """)


@APP.route('/rest/access/fail')
def rest_access_fail():
    """Recurso rest accesible."""
    resp = Response()
    resp.status_code = 200
    return resp


@APP.route('/rest/access/ok')
def rest_access_ok():
    """Recurso rest no accesible."""
    resp = Response()
    resp.status_code = 403
    return resp


@APP.route('/rest/insecure_accept/fail')
def rest_insecure_accept_fail():
    """Recurso rest accesible."""
    resp = Response()
    resp.status_code = 400
    return resp


@APP.route('/rest/insecure_accept/ok')
def rest_insecure_accept_ok():
    """Recurso rest no accesible."""
    resp = Response()
    resp.status_code = 406
    return resp


@APP.route('/rest/empty_content_type/fail')
def rest_empty_content_type_fail():
    """Check empty Content-Type."""
    resp = Response()
    resp.status_code = 400
    return resp


@APP.route('/rest/empty_content_type/ok')
def rest_empty_content_type_ok():
    """Check empty Content-Type."""
    resp = Response()
    resp.status_code = 415
    return resp


@APP.route('/rest/hsts/ok')
def rest_hsts_ok():
    """Header que define bien la implementacion de HSTS."""
    resp = Response('Expires OK')
    resp.headers['Strict-Transport-Security'] = 'max-age=31536000; \
        includeSubDomains; preload'
    return resp


@APP.route('/rest/hsts/fail')
def rest_hsts_fail():
    """Header que define mal implementacion de HSTS."""
    resp = Response('Expires FAIL')
    resp.headers['Strict-Transport-Security'] = 'Fail'
    return resp


def start():
    """Inicia el servidor de pruebas."""
    try:
        APP.run()
    except OSError:
        pass
