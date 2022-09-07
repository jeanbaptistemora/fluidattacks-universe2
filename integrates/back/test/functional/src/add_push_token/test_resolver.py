# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from . import (
    get_result,
)
from custom_exceptions import (
    StakeholderNotFound,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.stakeholders.types import (
    Stakeholder,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_push_token")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["user@gmail.com"],
        ["user_manager@gmail.com"],
        ["vulnerability_manager@gmail.com"],
        ["hacker@gmail.com"],
        ["reattacker@gmail.com"],
        ["resourcer@gmail.com"],
        ["reviewer@gmail.com"],
        ["service_forces@gmail.com"],
        ["customer_manager@fluidattacks.com"],
    ],
)
async def test_add_push_token(populate: bool, email: str) -> None:
    assert populate
    token = "ExponentPushToken[something123]"
    loaders: Dataloaders = get_new_context()
    stakeholder: Stakeholder = await loaders.stakeholder.load(email)
    if stakeholder.push_tokens:
        assert token not in stakeholder.push_tokens

    result: dict[str, Any] = await get_result(
        user=email,
        token=token,
    )
    assert "errors" not in result
    assert result["data"]["addPushToken"]["success"]

    loaders = get_new_context()
    stakeholder = await loaders.stakeholder.load(email)
    assert token in stakeholder.push_tokens


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_push_token")
@pytest.mark.parametrize(
    ["email"],
    [
        ["stakeholder_not_found@gmail.com"],
    ],
)
async def test_add_push_token_fail(populate: bool, email: str) -> None:
    assert populate
    token = "ExponentPushToken[something123]"
    result: dict[str, Any] = await get_result(
        user=email,
        token=token,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == str(StakeholderNotFound())
