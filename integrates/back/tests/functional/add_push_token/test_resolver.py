from . import (
    get_result,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_push_token")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["customer@gmail.com"],
        ["user_manager@gmail.com"],
        ["executive@gmail.com"],
        ["hacker@gmail.com"],
        ["rettacker@gmail.com"],
        ["resourcer@gmail.com"],
        ["reviewer@gmail.com"],
        ["service_forces@gmail.com"],
        ["customer_manager@fluidattacks.com"],
    ],
)
async def test_add_push_token(populate: bool, email: str) -> None:
    assert populate
    result: Dict[str, Any] = await get_result(
        user=email,
    )
    assert "errors" not in result
    assert result["data"]["addPushToken"]["success"]
