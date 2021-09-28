from . import (
    get_result,
)
from datetime import (
    datetime,
    timedelta,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("subscribe_to_entity_report")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["customer@gmail.com"],
        ["customeradmin@gmail.com"],
        ["executive@gmail.com"],
        ["hacker@gmail.com"],
        ["reattacker@gmail.com"],
        ["resourcer@gmail.com"],
        ["reviewer@gmail.com"],
        ["service_forces@gmail.com"],
        ["system_owner@gmail.com"],
    ],
)
async def test_subscribe_to_entity_report(populate: bool, email: str) -> None:
    assert populate
    organization: str = "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db"
    result: Dict[str, Any] = await get_result(
        user=email,
        org_id=organization,
    )
    print(result)
    assert "errors" not in result
    assert result["data"]["subscribeToEntityReport"]["success"]
