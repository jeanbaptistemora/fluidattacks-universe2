# Standard library
from functools import (
    partial,
)
from typing import (
    Callable,
    Dict,
    List,
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


def add_rule(
    finding: str,
    index: int,
    handler: Callable[[], Response],
) -> None:
    rule: str = f"/{finding}_{index}"
    endpoint: str = f"{finding}_{index}"
    APP.add_url_rule(rule, endpoint, handler)


@APP.route("/")
def home() -> Response:
    # Return a small sitemap with the available URL and methods in the server
    urls: List[str] = []

    for rule in APP.url_map.iter_rules():
        url = request.host_url[:-1] + urllib.parse.unquote(
            url_for(
                rule.endpoint,
                **{arg: f"[{arg}]" for arg in rule.arguments},
            )
        )
        urls.append(f'<a href={url}>{url}</a> {", ".join(rule.methods)}')

    content = f'<html><body>{"<br />".join(sorted(urls))}</body></html>'

    return Response(content, content_type="text/html")


def response_header(headers: Dict[str, str]) -> Response:
    return Response("<html></html>", headers=headers)


def _add_headers(
    finding: str,
    header: str,
    values: List[str],
) -> None:
    for index, value in enumerate(values):
        add_rule(finding, index, partial(response_header, {header: value}))


def add_f043_dast_csp_rules() -> None:
    _add_headers(
        "f043_dast_csp",
        "Content-Security-Policy",
        [
            "script-src;",
            "script-src *.domain.com;",
            "default-src 'self'",
            "default-src 'unsafe-eval'",
            "default-src 'unsafe-inline'",
            "default-src 'none'",
            "script-src data:",
            "script-src http:",
            "script-src https:",
            "script-src *.yandex.ru;",
            "frame-ancestors 'none'",
            "frame-ancestors 'self'",
            "upgrade-insecure-requests;",
            "block-all-mixed-content;",
        ],
    )


def add_f043_dast_rp_rules() -> None:
    _add_headers(
        "f043_dast_rp",
        "Referrer-Policy",
        [
            "",
            "out-of-spec",
            "out-of-spec, unsafe-url, same-origin",
            "out-of-spec, same-origin, unsafe-url",
        ],
    )


def add_f043_dast_sts_rules() -> None:
    _add_headers(
        "f043_dast_sts",
        "Strict-Transport-Security",
        [
            "",
            "max-age=31535999",
            "max-age=31536000",
        ],
    )


def add_f043_dast_xcto() -> None:
    _add_headers(
        "f043_dast_xcto",
        "X-Content-Type-Options",
        [
            "",
            "nosniff",
        ],
    )


def add_f043_dast_xfo() -> None:
    _add_headers(
        "f043_dast_xfo",
        "X-Frame-Options",
        [
            "",
            "deny",
            "sameorigin",
            "allow-from: DOMAIN",
        ],
    )


def start() -> None:
    APP.run()


add_f043_dast_csp_rules()
add_f043_dast_rp_rules()
add_f043_dast_sts_rules()
add_f043_dast_xcto()
add_f043_dast_xfo()
