from . import (
    get_result,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("invalidate_access_token")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["hacker@gmail.com"],
        ["reattacker@gmail.com"],
        ["customer@gmail.com"],
        ["customeradmin@gmail.com"],
        ["executive@gmail.com"],
        ["resourcer@gmail.com"],
        ["customer_manager@fluidattacks.com"],
        ["reviewer@gmail.com"],
        ["service_forces@gmail.com"],
        ["customer_manager@fluidattacks.com"],
    ],
)
async def test_invalidate_access_token(populate: bool, email: str) -> None:
    assert populate
    result: Dict[str, Any] = await get_result(
        user=email,
    )
    assert "errors" not in result
    assert result["data"]["invalidateAccessToken"]["success"]
