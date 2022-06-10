from . import (
    get_result,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("sign_in")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["hacker@gmail.com"],
        ["reattacker@gmail.com"],
        ["user@gmail.com"],
        ["user_manager@gmail.com"],
        ["vulnerability_manager@gmail.com"],
        ["resourcer@gmail.com"],
        ["customer_manager@fluidattacks.com"],
        ["reviewer@gmail.com"],
        ["service_forces@gmail.com"],
        ["customer_manager@fluidattacks.com"],
    ],
)
async def test_sign_in(populate: bool, email: str) -> None:
    assert populate
    result: Dict[str, Any] = await get_result(
        user=email,
    )
    assert "errors" not in result
    assert "success" in result["data"]["signIn"]
    assert not result["data"]["signIn"]["success"]
