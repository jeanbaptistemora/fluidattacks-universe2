from datetime import (
    datetime,
    timedelta,
)
from flask import (
    Flask,
    request,
    url_for,
)
from flask.wrappers import (
    Response,
)
from functools import (
    partial,
)
import os
import time
from typing import (
    Callable,
    List,
)
import urllib.parse

APP = Flask(__name__)
ROOT = os.path.dirname(__file__)

# Constants
HEADER_DATE_FMT: str = "%a, %d %b %Y %H:%M:%S GMT"


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


def _add_contents(finding: str, paths: List[str]) -> None:
    for index, path in enumerate(paths):
        with open(os.path.join(ROOT, path)) as handle:
            add_rule(
                finding,
                index,
                partial(Response, handle.read()),
            )


def _add_headers(
    finding: str,
    header: str,
    header_values: List[str],
    status: int = 200,
) -> None:
    for index, value in enumerate(header_values):
        add_rule(
            finding,
            index,
            partial(Response, headers={header: value}, status=status),
        )


def add_f015_dast_basic() -> None:
    _add_headers(
        finding="f015_dast_basic",
        header="WWW-Authenticate",
        header_values=[
            "",
            "Basic",
            "Basic realm=host.com",
            'Basic realm=host.com, charset="UTF-8"',
            'Bearer realm=host.com, charset="UTF-8"',
        ],
        status=401,
    )


def _add_f023_0() -> Response:
    # Perform a ugly injection
    if request.headers.get("host"):
        return Response(headers={"Location": request.host_url})
    return Response()


def _add_f023_1() -> Response:
    # Redirects to other "safe" url
    if request.headers.get("host"):
        return Response(headers={"Location": "http://localhost"})
    return Response()


def add_f023() -> None:
    for index, rule in enumerate([_add_f023_0, _add_f023_1]):
        add_rule(
            finding="f023",
            index=index,
            handler=rule,
        )


def add_f036() -> None:
    _add_contents(
        finding="f036",
        paths=[
            "templates/f036_0.html",
        ],
    )


def add_f042_secure() -> None:
    _add_headers(
        "f042_secure",
        "Set-Cookie",
        [
            "session=test; Secure",
            "google_analytics=1asdf34; Secure",
            "session=test",
            "session=test",
            "google_analytics=1asdf34",
            "action=test; HttpOnly",
            "google_analytics=",
        ],
    )


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


def _add_f064_server_clock_1() -> Response:
    gmt = time.gmtime()
    gmt_str = time.strftime(HEADER_DATE_FMT, gmt)
    date = datetime.strptime(gmt_str, HEADER_DATE_FMT) - timedelta(hours=1)
    return Response(headers={"Date": date.strftime(HEADER_DATE_FMT)})


def add_f064_server_clock() -> None:
    _add_headers(
        "f064_server_clock",
        "Date",
        [
            "",
        ],
    )
    add_rule(
        finding="f064_server_clock",
        index=1,
        handler=_add_f064_server_clock_1,
    )


def add_f086() -> None:
    _add_contents(
        finding="f086",
        paths=[
            "templates/f086_0.html",
        ],
    )


def start() -> None:
    APP.run()


add_f015_dast_basic()
add_f023()
add_f036()
add_f042_secure()
add_f043_dast_csp_rules()
add_f043_dast_rp_rules()
add_f043_dast_sts_rules()
add_f043_dast_xcto()
add_f043_dast_xfo()
add_f064_server_clock()
add_f086()
