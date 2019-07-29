# -*- coding: utf-8 -*-

"""Stop test mocks."""

# standard imports
import pytest


@pytest.mark.teardown
def test_teardown(stop_mocks):
    """Teardown fixture."""
    assert True
