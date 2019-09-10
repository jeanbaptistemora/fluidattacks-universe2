"""Test the GraphQL module."""

# standard imports
import textwrap

# 3rd party imports

# local imports
from fluidasserts.proto import graphql


#
# Constants
#


SEC_URL = 'http://localhost:4001/secure-graphql'
INSEC_URL = 'http://localhost:4001/insecure-graphql'
LAZY_URL = 'http://localhost:4001/lazy-graphql'

BAD_URL = 'http://asdf:4001/secure-graphql'
BAD_PARAM_URL = 'localhost:4001/secure-graphql'
BAD_JSON_URL = 'http://localhost:4001/errors/invalid-json'

QUERY = textwrap.dedent("""
    {
        users {
            cpus
            distros {
                name
            }
        }
    }
    """)


#
# Test OPEN
#

def test_accepts_introspection_open():
    """Test accepts_introspection."""
    assert graphql.accepts_introspection(INSEC_URL).is_open()


def test_has_dos_open():
    """Test has_dos."""
    assert graphql.has_dos(
        url=LAZY_URL, query=QUERY, num=1, timeout=1.0).is_open()


#
# Test CLOSED
#


def test_accepts_introspection_closed():
    """Test accepts_introspection."""
    assert graphql.accepts_introspection(SEC_URL).is_closed()


def test_has_dos_closed():
    """Test has_dos."""
    assert graphql.has_dos(
        url=SEC_URL, query=QUERY, num=1, timeout=10.0).is_closed()


#
# Test UNKNOWN
#


def test_accepts_introspection_unknown():
    """Test accepts_introspection."""
    assert graphql.accepts_introspection(BAD_URL).is_unknown()
    assert graphql.accepts_introspection(BAD_JSON_URL).is_unknown()
    assert graphql.accepts_introspection(BAD_PARAM_URL).is_unknown()


def test_has_dos_unknown():
    """Test has_dos."""
    for url in (BAD_URL, BAD_PARAM_URL):
        assert graphql.has_dos(
            url=url, query=QUERY, num=1, timeout=10.0).is_unknown()
