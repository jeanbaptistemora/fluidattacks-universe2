# Third party libraries
from flask import (
    Flask,
)


APP = Flask(__name__)


@APP.route('/')
def home() -> str:
    return 'Welcome!'


def start() -> None:
    APP.run()
