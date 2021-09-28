from . import (
    get_result,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("acknowledge_concurrent_session")
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
        ["system_owner@gmail.com"],
        ["reviewer@gmail.com"],
        ["service_forces@gmail.com"],
        ["system_owner@gmail.com"],
    ],
)
async def test_acknowledge_concurrent_session(
    populate: bool, email: str
) -> None:
    assert populate
    result: Dict[str, Any] = await get_result(
        user=email,
    )
    assert "errors" not in result
    assert result["data"]["acknowledgeConcurrentSession"]["success"]
