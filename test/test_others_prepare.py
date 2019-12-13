# -*- coding: utf-8 -*-

"""Prepare test mocks."""

# standard imports
import pytest


@pytest.mark.prepare
def test_prepare(run_mocks):
    """Setting fixture."""
    assert True
