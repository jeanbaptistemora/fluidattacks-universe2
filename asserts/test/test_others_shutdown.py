# -*- coding: utf-8 -*-

"""Stop test mocks."""

# standard imports
import pytest


@pytest.mark.shutdown
def test_shutdown(stop_mocks):
    """Shutdown fixture."""
    assert True
