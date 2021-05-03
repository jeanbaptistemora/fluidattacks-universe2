# Standard library
from textwrap import (
    dedent,
)
from typing import (
    Optional,
)

# Third party libraries
import pytest

# Local libraries
from http_headers import (
    as_string,
    content_security_policy,
    strict_transport_security,
    referrer_policy,
    www_authenticate,
    x_content_type_options,
    x_frame_options,
)
from http_headers.types import (
    WWWAuthenticate,
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
            chars_per_line=40,
        )
        == dedent(
            """
        ¦ line ¦ Data                                     ¦
        ¦ ---- ¦ ---------------------------------------- ¦
        ¦    1 ¦ > GET fluidattacks.com                   ¦
        ¦    2 ¦ > ...                                    ¦
        ¦    3 ¦                                          ¦
        ¦    4 ¦ < Transfer-Encoding: chunked             ¦
        ¦  > 5 ¦ < Connection: keep-alive                 ¦
        ¦    6 ¦ < Cache-Control: max-age=3600            ¦
        ¦    7 ¦ < Server: cloudflare                     ¦
        ¦    8 ¦                                          ¦
        ¦    9 ¦ * EOF                                    ¦
        ¦ ---- ¦ ---------------------------------------- ¦
               ^ Column 0
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
            chars_per_line=40,
        )
        == dedent(
            """
        ¦ line ¦ Data                                     ¦
        ¦ ---- ¦ ---------------------------------------- ¦
        ¦    4 ¦ < Transfer-Encoding: chunked             ¦
        ¦    5 ¦ < Connection: keep-alive                 ¦
        ¦    6 ¦ < Cache-Control: max-age=3600            ¦
        ¦    7 ¦ < Server: cloudflare                     ¦
        ¦    8 ¦                                          ¦
        ¦  > 9 ¦ * EOF                                    ¦
        ¦ ---- ¦ ---------------------------------------- ¦
               ^ Column 0
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
            chars_per_line=40,
        )
        == dedent(
            """
        ¦ line ¦ Data                                     ¦
        ¦ ---- ¦ ---------------------------------------- ¦
        ¦    9 ¦     ------------------------------------ ¦
        ¦   10 ¦     ------------------------------------ ¦
        ¦   11 ¦     ------                               ¦
        ¦   12 ¦ < Server: cloudflare                     ¦
        ¦   13 ¦                                          ¦
        ¦ > 14 ¦ * EOF                                    ¦
        ¦ ---- ¦ ---------------------------------------- ¦
               ^ Column 0
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
            chars_per_line=40,
        )
        == dedent(
            """
        ¦ line ¦ Data                                     ¦
        ¦ ---- ¦ ---------------------------------------- ¦
        ¦    1 ¦ > GET fluidattacks.com                   ¦
        ¦    2 ¦ > ...                                    ¦
        ¦    3 ¦                                          ¦
        ¦    4 ¦ < Transfer-Encoding: chunked             ¦
        ¦    5 ¦ < Connection: keep-alive                 ¦
        ¦  > 6 ¦ < Cache-Control:                         ¦
        ¦    7 ¦     ------------------------------------ ¦
        ¦    8 ¦     ------------------------------------ ¦
        ¦    9 ¦     ------------------------------------ ¦
        ¦   10 ¦     ------------------------------------ ¦
        ¦   11 ¦     ------                               ¦
        ¦   12 ¦ < Server: cloudflare                     ¦
        ¦   13 ¦                                          ¦
        ¦   14 ¦ * EOF                                    ¦
        ¦ ---- ¦ ---------------------------------------- ¦
               ^ Column 0
    """
        )[1:-1]
    )


@pytest.mark.skims_test_group("unittesting")
def test_content_security_policy() -> None:
    parse = content_security_policy.parse

    header = parse(
        (
            "content-security-policy:   script-src 'self'  'unsafe-inline' "
            "localhost:* cdn.announcekit.app  ;"
        )
    )
    assert header.directives == {
        "script-src": [
            "'self'",
            "'unsafe-inline'",
            "localhost:*",
            "cdn.announcekit.app",
        ],
    }

    header = parse("Content-Security-Policy: upgrade-insecure-requests;")
    assert header.directives == {"upgrade-insecure-requests": []}


@pytest.mark.skims_test_group("unittesting")
def test_referrer_policy() -> None:
    # Header names are caseless
    parse = referrer_policy.parse

    header = parse("  referrer-pOlicy  :  no-referreR,wrong,, strict-origin ")
    assert header.values == ["no-referrer", "wrong", "strict-origin"]

    header = parse("referrer-policy:")
    assert header.values == []

    header = parse("wrong:")
    assert not header


@pytest.mark.skims_test_group("unittesting")
def test_strict_transport_security() -> None:
    # Header names are caseless
    parse = strict_transport_security.parse

    header = parse("  strict-transport-security  :  max-age  =  123  ")
    assert not header.include_sub_domains
    assert header.max_age == 123
    assert not header.preload

    header = parse("Strict-Transport-Security: max-age=123; includeSubDomains")
    assert header.include_sub_domains
    assert header.max_age == 123
    assert not header.preload

    header = parse("Strict-Transport-Security:max-age=123;preload")
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
                type="Basic",
            ),
        ),
        (
            'www-authenticAte: Bearer realm="host.com", charset="UTF-8"',
            WWWAuthenticate(
                name="www-authenticAte",
                charset='"UTF-8"',
                realm='"host.com"',
                type="Bearer",
            ),
        ),
    ],
)
def test_www_authenticate(
    line: str,
    expected: Optional[WWWAuthenticate],
) -> None:
    assert www_authenticate.parse(line) == expected


@pytest.mark.skims_test_group("unittesting")
def test_x_content_type_options() -> None:
    parse = x_content_type_options.parse

    header = parse("  x-content-type-options  :  VALUE  ")
    assert header.value == "value"

    header = parse("  x-content-tpe-options  :  VALUE  ")
    assert not header


@pytest.mark.skims_test_group("unittesting")
def test_x_frame_options() -> None:
    # Header names are caseless
    parse = x_frame_options.parse

    header = parse("  x-frame-options  :  deny  ")
    assert header.value == "deny"
