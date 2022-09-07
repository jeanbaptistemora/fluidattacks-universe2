# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from . import (
    get_result,
)
from dataloaders import (
    get_new_context,
)
from db_model.stakeholders.types import (
    Stakeholder,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_stakeholder")
async def test_admin(populate: bool) -> None:
    assert populate
    email = "new_user_test@gmai.com"
    role = "USER"
    result: Dict[str, Any] = await get_result(email=email, role=role)
    assert "errors" not in result
    assert result["data"]["addStakeholder"]["success"]
    loaders = get_new_context()
    stakeholder: Stakeholder = await loaders.stakeholder.load(email)
    assert stakeholder.email == email
