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
@pytest.mark.resolver_test_group("accept_legal")
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
async def test_accept_legal(populate: bool, email: str) -> None:
    assert populate
    result: Dict[str, Any] = await get_result(
        user=email,
    )
    assert "errors" not in result
    assert result["data"]["acceptLegal"]["success"]
