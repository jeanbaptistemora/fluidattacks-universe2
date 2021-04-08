# Third party libraries
import pytest

# Local libraries
from http_headers import (
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
