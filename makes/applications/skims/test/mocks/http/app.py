# Third party libraries
from flask import Flask


APP = Flask(__name__)


@APP.route('/')
def home():
    return 'Welcome!'


def start():
    APP.run()
