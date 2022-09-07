# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from forces.apis.integrates import (
    get_api_token,
    INTEGRATES_API_TOKEN,
    set_api_token,
)
import pytest


@pytest.mark.first
def test_get_api_token() -> None:
    try:
        get_api_token()
        assert False
    except LookupError:
        assert True


@pytest.mark.last
def test_set_api_token(test_token: str) -> None:
    set_api_token(test_token)
    assert INTEGRATES_API_TOKEN.get() == test_token
