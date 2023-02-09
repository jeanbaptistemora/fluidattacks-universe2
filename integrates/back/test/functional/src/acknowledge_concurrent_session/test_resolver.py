from . import (
    get_result,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("acknowledge_concurrent_session")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["hacker@gmail.com"],
        ["reattacker@gmail.com"],
        ["user@gmail.com"],
        ["user_manager@gmail.com"],
        ["resourcer@gmail.com"],
        ["customer_manager@fluidattacks.com"],
        ["reviewer@gmail.com"],
        ["service_forces@gmail.com"],
        ["vulnerability_manager@gmail.com"],
    ],
)
async def test_acknowledge_concurrent_session(
    populate: bool, email: str
) -> None:
    assert populate
    result: dict[str, Any] = await get_result(
        user=email,
    )
    assert "errors" not in result
    assert result["data"]["acknowledgeConcurrentSession"]["success"]

    loaders: Dataloaders = get_new_context()
    stakeholder = await loaders.stakeholder.load(email)
    assert stakeholder
    assert stakeholder.is_concurrent_session is False
