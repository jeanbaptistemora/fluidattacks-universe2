# Standard library
from functools import (
    partial,
)
from typing import (
    Dict,
)
import urllib.parse

# Third party libraries
from flask import (
    Flask,
    request,
    url_for,
)
from flask.wrappers import (
    Response,
)


APP = Flask(__name__)


@APP.route('/')
def home() -> str:
    return '\n'.join(sorted(
        f'{request.host_url[:-1]}{urllib.parse.unquote(url)} {rule.methods}'
        for rule in APP.url_map.iter_rules()
        for url in [url_for(rule.endpoint, **{
            arg: f'[{arg}]' for arg in rule.arguments
        })]
    ))


def configure_f043_dast_sts() -> None:

    def generator(headers: Dict[str, str]) -> Response:
        return Response(headers=headers)

    for index, headers in enumerate([
        {},
        {'Strict-Transport-Security': ''},
        {'Strict-Transport-Security': 'max-age=31535999'},
        {'Strict-Transport-Security': 'max-age=31536000'},
    ]):
        APP.add_url_rule(
            f'/f043_dast_sts_{index}',
            f'_f043_dast_sts_{index}',
            partial(generator, headers=headers),
        )


def start() -> None:
    APP.run()


configure_f043_dast_sts()
