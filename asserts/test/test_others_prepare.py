# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# -*- coding: utf-8 -*-

"""Prepare test mocks."""


import pytest


@pytest.mark.prepare
def test_prepare(run_mocks):
    """Setting fixture."""
    assert True
