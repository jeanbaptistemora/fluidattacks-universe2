# Standard library
from textwrap import (
    dedent,
)

# Third party libraries
from aioextensions import (
    run_decorator,
)
import pytest

# Local libraries
from http_headers import (
    as_string,
    from_url,
    strict_transport_security,
    referrer_policy,
)


@pytest.mark.skims_test_group('unittesting')
def test_as_string() -> None:
    assert as_string.snippet(
        url='fluidattacks.com',
        header='Connection',
        headers={
            'Transfer-Encoding': 'chunked',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=3600',
            'Server': 'cloudflare',
        },
        chars_per_line=40,
    ) == dedent("""
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
    """)[1:-1]

    assert as_string.snippet(
        url='fluidattacks.com',
        header='X-not-found',
        headers={
            'Transfer-Encoding': 'chunked',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=3600',
            'Server': 'cloudflare',
        },
        chars_per_line=40,
    ) == dedent("""
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
    """)[1:-1]


@pytest.mark.skims_test_group('unittesting')
def test_referrer_policy() -> None:
    # Header names are caseless
    parse = referrer_policy.parse

    header = parse('  referrer-pOlicy  :  no-referreR,wrong,, strict-origin ')
    assert header.values == ["no-referrer", "wrong", "strict-origin"]

    header = parse('referrer-policy:')
    assert header.values == []

    header = parse('wrong:')
    assert not header


@pytest.mark.skims_test_group('unittesting')
def test_strict_transport_security() -> None:
    # Header names are caseless
    parse = strict_transport_security.parse

    header = parse('  strict-transport-security  :  max-age  =  123  ')
    assert not header.include_sub_domains
    assert header.max_age == 123
    assert not header.preload

    header = parse('Strict-Transport-Security: max-age=123; includeSubDomains')
    assert header.include_sub_domains
    assert header.max_age == 123
    assert not header.preload

    header = parse('Strict-Transport-Security:max-age=123;preload')
    assert not header.include_sub_domains
    assert header.max_age == 123
    assert header.preload

    header = parse('Strict-Transport-Security: preload')
    assert not header

    header = parse('Strict-Transport-Security-: preload')
    assert not header


@run_decorator
@pytest.mark.skims_test_group('unittesting')
async def test_from_url() -> None:
    headers = await from_url.get('GET', 'http://fluidattacks.com')

    assert 'Content-Type' in headers
