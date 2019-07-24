"""Test the GraphQL module."""

# standard imports

# 3rd party imports
import pytest

# local imports
from fluidasserts.proto import graphql


#
# Constants
#


SEC_URL = 'http://localhost:4001/secure-graphql'
INSEC_URL = 'http://localhost:4001/insecure-graphql'

BAD_URL = 'http://asdf:4001/secure-graphql'
BAD_PARAM_URL = 'localhost:4001/secure-graphql'
BAD_JSON_URL = 'http://localhost:4001/errors/invalid-json'


#
# Test OPEN
#

def test_accepts_introspection_open():
    """Test accepts_introspection."""
    assert graphql.accepts_introspection(INSEC_URL).is_open()


#
# Test CLOSED
#


def test_accepts_introspection_closed():
    """Test accepts_introspection."""
    assert graphql.accepts_introspection(SEC_URL).is_closed()


#
# Test UNKNOWN
#


def test_accepts_introspection_unknown():
    """Test accepts_introspection."""
    assert graphql.accepts_introspection(BAD_URL).is_unknown()
    assert graphql.accepts_introspection(BAD_JSON_URL).is_unknown()
    assert graphql.accepts_introspection(BAD_PARAM_URL).is_unknown()
