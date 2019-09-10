# -*- coding: utf-8 -*-

"""Camera mocks."""

# standard imports

# 3rd party imports
from flask import Flask
from flask import request
from flask import Response


# local imports
# none


APP = Flask(__name__, static_folder='static', static_url_path='/static')


@APP.route('/httpDisabled.shtml', methods=['GET'])
def axis_rce():
    """Start Axis camera."""
    if request.values['http_user'] == '%p|%p':
        resp = Response()
        resp.status_code = 500
        return resp
    return 'Everything\'s OK'


def start():
    """Start server."""
    try:
        APP.run(port=9001)
    except OSError:
        pass
