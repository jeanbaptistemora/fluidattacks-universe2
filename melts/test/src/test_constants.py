# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from toolbox import (
    constants,
)


def test_constants_api_token() -> None:
    """Test constants.API_TOKEN."""
    assert constants.API_TOKEN
