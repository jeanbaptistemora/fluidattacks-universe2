# Third party libraries
from aioextensions import (
    run_decorator,
)
import pytest

# Local libraries
from http_headers import (
    from_url,
    strict_transport_security,
)


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
