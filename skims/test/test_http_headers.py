# pylint: disable=too-many-statements
from datetime import (
    datetime,
    timezone,
)
from http_headers import (
    as_string,
    content_security_policy,
    date,
    referrer_policy,
    set_cookie,
    strict_transport_security,
    www_authenticate,
    x_content_type_options,
    x_frame_options,
)
from http_headers.types import (
    DateHeader,
    WWWAuthenticate,
)
import pytest
from textwrap import (
    dedent,
)


@pytest.mark.skims_test_group("unittesting")
def test_as_string() -> None:
    assert (
        as_string.snippet(
            url="fluidattacks.com",
            header="Connection",
            headers={
                "Transfer-Encoding": "chunked",
                "Connection": "keep-alive",
                "Cache-Control": "max-age=3600",
                "Server": "cloudflare",
            },
            columns_per_line=40,
        )
        == dedent(
            """
              1 | > GET fluidattacks.com
              2 | > ...
              3 |
              4 | < Transfer-Encoding: chunked
            > 5 | < Connection: keep-alive
              6 | < Cache-Control: max-age=3600
              7 | < Server: cloudflare
              8 |
              9 | * EOF
                ^ Col 0
            """
        )[1:-1]
    )

    assert (
        as_string.snippet(
            url="fluidattacks.com",
            header="X-not-found",
            headers={
                "Transfer-Encoding": "chunked",
                "Connection": "keep-alive",
                "Cache-Control": "max-age=3600",
                "Server": "cloudflare",
            },
            columns_per_line=40,
        )
        == dedent(
            """
              1 | > GET fluidattacks.com
              2 | > ...
              3 |
              4 | < Transfer-Encoding: chunked
              5 | < Connection: keep-alive
              6 | < Cache-Control: max-age=3600
              7 | < Server: cloudflare
              8 |
            > 9 | * EOF
                ^ Col 0
            """
        )[1:-1]
    )

    assert (
        as_string.snippet(
            url="fluidattacks.com",
            header="X-not-found",
            headers={
                "Transfer-Encoding": "chunked",
                "Connection": "keep-alive",
                "Cache-Control": "-" * 150,
                "Server": "cloudflare",
            },
            columns_per_line=40,
        )
        == dedent(
            """
               1 | > GET fluidattacks.com
               2 | > ...
               3 |
               4 | < Transfer-Encoding: chunked
               5 | < Connection: keep-alive
               6 | < Cache-Control:
               7 |     ------------------------------------
               8 |     ------------------------------------
               9 |     ------------------------------------
              10 |     ------------------------------------
              11 |     ------
              12 | < Server: cloudflare
              13 |
            > 14 | * EOF
                 ^ Col 0
            """
        )[1:-1]
    )

    assert (
        as_string.snippet(
            url="fluidattacks.com",
            header="Cache-Control",
            headers={
                "Transfer-Encoding": "chunked",
                "Connection": "keep-alive",
                "Cache-Control": "-" * 150,
                "Server": "cloudflare",
            },
            columns_per_line=40,
        )
        == dedent(
            """
               1 | > GET fluidattacks.com
               2 | > ...
               3 |
               4 | < Transfer-Encoding: chunked
               5 | < Connection: keep-alive
            >  6 | < Cache-Control:
               7 |     ------------------------------------
               8 |     ------------------------------------
               9 |     ------------------------------------
              10 |     ------------------------------------
              11 |     ------
              12 | < Server: cloudflare
              13 |
              14 | * EOF
                 ^ Col 0
            """
        )[1:-1]
    )


@pytest.mark.skims_test_group("unittesting")
def test_content_security_policy() -> None:
    parse = content_security_policy.parse

    header = parse(
        (
            "content-security-policy:   script-src 'self'  'unsafe-inline' "
            "localhost:* cdn.announcekit.app,"
        )
    )
    assert header is not None
    assert header.directives == {
        "script-src": [
            "'self'",
            "'unsafe-inline'",
            "localhost:*",
            "cdn.announcekit.app",
        ],
    }

    header = parse("Content-Security-Policy: upgrade-insecure-requests;")
    assert header is not None
    assert header.directives == {"upgrade-insecure-requests": []}


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.parametrize(
    "line,expected",
    [
        ("date:", None),
        ("Date: Wed, 21 Oct 2015 07:28:00", None),
        (
            "Date: Wed, 21 Oct 2015 07:28:00 GMT",
            DateHeader(
                name="Date",
                date=datetime(2015, 10, 21, 7, 28, 0, tzinfo=timezone.utc),
            ),
        ),
    ],
)
def test_date(
    line: str,
    expected: DateHeader | None,
) -> None:
    assert date.parse(line) == expected


@pytest.mark.skims_test_group("unittesting")
def test_referrer_policy() -> None:
    # Header names are caseless
    parse = referrer_policy.parse

    header = parse("  referrer-pOlicy  :  no-referreR,wrong,, strict-origin ")
    assert header is not None
    assert header.values == ["no-referrer", "wrong", "strict-origin"]

    header = parse("referrer-policy:")
    assert header is not None
    assert header.values == []

    header = parse("wrong:")
    assert not header


@pytest.mark.skims_test_group("unittesting")
def test_set_cookie() -> None:
    # Header names are caseless
    parse = set_cookie.parse

    header = parse("  set-cookie  :  key  =  value  ")
    assert header is not None
    assert header.raw_content == "key  =  value"
    assert header.name == "set-cookie"
    assert header.cookie_name == "key"
    assert header.cookie_value == "value"
    assert not header.secure
    assert not header.httponly
    assert header.samesite == "None"

    header = parse("  set-cookie  :  key  =  value  ;  Secure  ")
    assert header is not None
    assert header.raw_content == "key  =  value  ;  Secure"
    assert header.name == "set-cookie"
    assert header.cookie_name == "key"
    assert header.cookie_value == "value"
    assert header.secure
    assert not header.httponly
    assert header.samesite == "None"

    header = parse("  set-cookie  :  key  =  value  Secure  ")
    assert header is not None
    assert header.raw_content == "key  =  value  Secure"
    assert header.name == "set-cookie"
    assert header.cookie_name == "key"
    assert header.cookie_value == "value  Secure"
    assert not header.secure
    assert not header.httponly
    assert header.samesite == "None"

    header = parse("  set-cookie  :  key  =  ")
    assert header is not None
    assert header.raw_content == "key  ="
    assert header.name == "set-cookie"
    assert header.cookie_name == "key"
    assert header.cookie_value == ""
    assert not header.secure
    assert not header.httponly
    assert header.samesite == "None"

    header = parse("  set-cookie  :  key  =  value  ;  HttpOnly  ")
    assert header is not None
    assert header.name == "set-cookie"
    assert header.cookie_name == "key"
    assert header.cookie_value == "value"
    assert not header.secure
    assert header.httponly
    assert header.samesite == "None"

    header = parse("  set-cookie  :  key  =  value  ;  SameSite = Strict  ")
    assert header is not None
    assert header.name == "set-cookie"
    assert header.cookie_name == "key"
    assert header.cookie_value == "value"
    assert not header.secure
    assert not header.httponly
    assert header.samesite == "Strict"

    header = parse("  set-cookie  :  key  =  value  ;  SameSite = Lax  ")
    assert header is not None
    assert header.name == "set-cookie"
    assert header.cookie_name == "key"
    assert header.cookie_value == "value"
    assert not header.secure
    assert not header.httponly
    assert header.samesite == "Lax"

    header = parse("  set-cookie  :  key  =  value  ;  SameSite = None  ")
    assert header is not None
    assert header.name == "set-cookie"
    assert header.cookie_name == "key"
    assert header.cookie_value == "value"
    assert not header.secure
    assert not header.httponly
    assert header.samesite == "None"

    header = parse(
        "  set-cookie  :  key  =  value  ;  Secure;  SameSite = None  "
    )
    assert header is not None
    assert header.name == "set-cookie"
    assert header.cookie_name == "key"
    assert header.cookie_value == "value"
    assert header.secure
    assert not header.httponly
    assert header.samesite == "None"

    header = parse(
        "set-cookie  :  key  =  value;  Secure;  HttpOnly; SameSite  =  Strict"
    )
    assert header is not None
    assert header.name == "set-cookie"
    assert header.cookie_name == "key"
    assert header.cookie_value == "value"
    assert header.secure
    assert header.httponly
    assert header.samesite == "Strict"


@pytest.mark.skims_test_group("unittesting")
def test_strict_transport_security() -> None:
    # Header names are caseless
    parse = strict_transport_security.parse

    header = parse("  strict-transport-security  :  max-age  =  123  ")
    assert header is not None
    assert not header.include_sub_domains
    assert header.max_age == 123
    assert not header.preload

    header = parse("Strict-Transport-Security: max-age=123; includeSubDomains")
    assert header is not None
    assert header.include_sub_domains
    assert header.max_age == 123
    assert not header.preload

    header = parse("Strict-Transport-Security:max-age=123;preload")
    assert header is not None
    assert not header.include_sub_domains
    assert header.max_age == 123
    assert header.preload

    header = parse("Strict-Transport-Security: preload")
    assert not header

    header = parse("Strict-Transport-Security-: preload")
    assert not header


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.parametrize(
    "line,expected",
    [
        ("www-authenticate:", None),
        ("www-authenticate: Basic", None),
        (
            "www-authenticate: Basic realm=host.com",
            WWWAuthenticate(
                name="www-authenticate",
                charset="",
                realm="host.com",
                type="basic",
            ),
        ),
        (
            'www-authenticAte: Bearer realm="host.com", charset="UTF-8"',
            WWWAuthenticate(
                name="www-authenticAte",
                charset='"UTF-8"',
                realm='"host.com"',
                type="bearer",
            ),
        ),
    ],
)
def test_www_authenticate(
    line: str,
    expected: WWWAuthenticate | None,
) -> None:
    assert www_authenticate.parse(line) == expected


@pytest.mark.skims_test_group("unittesting")
def test_x_content_type_options() -> None:
    parse = x_content_type_options.parse

    header = parse("  x-content-type-options  :  VALUE  ")
    assert header is not None
    assert header.value == "value"

    header = parse("  x-content-tpe-options  :  VALUE  ")
    assert not header


@pytest.mark.skims_test_group("unittesting")
def test_x_frame_options() -> None:
    # Header names are caseless
    parse = x_frame_options.parse

    header = parse("  x-frame-options  :  deny  ")
    assert header is not None
    assert header.value == "deny"
