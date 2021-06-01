# -*- coding: utf-8 -*-

"""Camera mocks."""


import contextlib
from flask import (
    Flask,
    request,
    Response,
)

# none


APP = Flask(__name__, static_folder="static", static_url_path="/static")


@APP.route("/httpDisabled.shtml", methods=["GET"])
def axis_rce():
    """Start Axis camera."""
    if request.values["http_user"] == "%p|%p":
        resp = Response()
        resp.status_code = 500
        return resp
    return "Everything's OK"


def start():
    """Start server."""
    with contextlib.suppress(OSError):
        APP.run(port=9001)
