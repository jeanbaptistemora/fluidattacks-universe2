# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from . import (
    get_result,
)
from dataloaders import (
    get_new_context,
)
from mailer.findings import (
    send_mail_new_draft,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("submit_draft")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
    ],
)
async def test_submit_draft(populate: bool, email: str) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    result: Dict[str, Any] = await get_result(
        user=email, finding_id=finding_id
    )
    await send_mail_new_draft(
        get_new_context(),
        finding_id,
        "001. SQL injection - C Sharp SQL API",
        "group1",
        email,
    )
    assert "errors" not in result
    assert result["data"]["submitDraft"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("submit_draft")
@pytest.mark.parametrize(
    ["email"],
    [
        ["hacker@gmail.com"],
    ],
)
async def test_submit_draft_fail_1(populate: bool, email: str) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    result: Dict[str, Any] = await get_result(
        user=email, finding_id=finding_id
    )
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "Exception - This draft has already been submitted"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("submit_draft")
@pytest.mark.parametrize(
    ["email"],
    [
        ["user@gmail.com"],
    ],
)
async def test_submit_draft_fail_2(populate: bool, email: str) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    result: Dict[str, Any] = await get_result(
        user=email, finding_id=finding_id
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
