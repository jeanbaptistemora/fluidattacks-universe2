# -*- coding: utf-8 -*-

"""Softphone mocks."""

# standard imports
import base64

# 3rd party imports
from flask import Flask
from flask import request


# local imports
# none


APP = Flask(__name__, static_folder='static', static_url_path='/static')


@APP.route('/')
def home():
    """Respuesta a directorio raiz."""
    return 'Mock SIP'


@APP.route('/index.cmd')
def unify_login_home():
    """Return Unify login home."""
    return 'OpenScape Desk Phone IP Admin'


@APP.route('/page.cmd', methods=['POST'])
def unify_login_action_ok():
    """Validate default password."""
    if request.values['AdminPassword'] == '123456':
        return 'Login OK'
    return "action='./page.cmd'"


@APP.route('/login.htm')
def polycom_login_home():
    """Return Polycom login home."""
    return 'Polycom Web Configuration Utility'


@APP.route('/auth.htm')
def polycom_login_action_ok():
    """Validate default password."""
    auth_header = request.headers['Authorization']
    encoded_pass = auth_header.split(' ')[1]
    decoded_pass = base64.b64decode(encoded_pass)
    if decoded_pass == b'Polycom:456':
        return "SoundStation IP 6000"
    return "Login failed"


def start():
    """Inicia el servidor de pruebas."""
    try:
        APP.run(port=8001)
    except OSError:
        pass
