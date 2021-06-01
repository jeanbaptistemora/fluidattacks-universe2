# -*- coding: utf-8 -*-

"""Stop test mocks."""


import pytest


@pytest.mark.shutdown
def test_shutdown(stop_mocks):
    """Shutdown fixture."""
    assert True
