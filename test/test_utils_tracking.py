# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.utils.tracking."""

# standard imports
import os
from contextlib import contextmanager

# 3rd party imports

# local imports
from fluidasserts.utils import tracking


#
# Helpers
#


@contextmanager
def enabled_tracking():
    """Temporarily enable tracking."""
    previous_value: str = os.environ['FA_NOTRACK']
    os.environ['FA_NOTRACK'] = 'false'
    try:
        yield
    finally:
        os.environ['FA_NOTRACK'] = previous_value


@contextmanager
def disabled_tracking():
    """Temporarily enable tracking."""
    previous_value: str = os.environ['FA_NOTRACK']
    os.environ['FA_NOTRACK'] = 'true'
    try:
        yield
    finally:
        os.environ['FA_NOTRACK'] = previous_value


#
# Tests
#


def test_get_os_fingerprint():
    """Test get_os_fingerprint."""
    assert isinstance(tracking.get_os_fingerprint(), str)


def test_mp_track():
    """Test mp_track."""
    with enabled_tracking():
        assert tracking.mp_track('test')
    with disabled_tracking():
        assert tracking.mp_track('test')
