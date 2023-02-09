from . import (
    get_result,
)
from dataloaders import (
    get_new_context,
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
    assert "addStakeholder" in result["data"]
    assert "success" in result["data"]["addStakeholder"]
    assert result["data"]["addStakeholder"]["success"]
    loaders = get_new_context()
    stakeholder = await loaders.stakeholder.load(email)
    assert stakeholder
    assert stakeholder.email == email
