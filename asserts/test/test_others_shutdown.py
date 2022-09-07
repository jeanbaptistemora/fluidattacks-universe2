# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# -*- coding: utf-8 -*-

"""Stop test mocks."""


import pytest


@pytest.mark.shutdown
def test_shutdown(stop_mocks):
    """Shutdown fixture."""
    assert True
