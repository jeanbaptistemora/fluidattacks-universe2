# -*- coding: utf-8 -*-

"""Camera mocks."""

# standard imports
import contextlib

# 3rd party imports
from flask import Flask


# local imports
# none


APP = Flask(__name__, static_folder="static", static_url_path="/static")


@APP.route("/httpDisabled.shtml", methods=["GET"])
def axis_rce():
    """Start Axis camera."""
    return "Everything's OK"


def start():
    """Start server."""
    with contextlib.suppress(OSError):
        APP.run(port=9002)
