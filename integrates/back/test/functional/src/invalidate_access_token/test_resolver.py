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
@pytest.mark.resolver_test_group("invalidate_access_token")
@pytest.mark.parametrize(
    ["email", "iat"],
    [
        ["admin@gmail.com", 1634677195],
        ["hacker@gmail.com", 1634677195],
        ["reattacker@gmail.com", 1657298463],
        ["user@gmail.com", 1657298264],
        ["user_manager@gmail.com", 1657298299],
        ["vulnerability_manager@gmail.com", 1657298346],
        ["resourcer@gmail.com", 1657298463],
        ["reviewer@gmail.com", 1657295874],
        ["service_forces@gmail.com", 1657278953],
        ["customer_manager@fluidattacks.com", 1657287433],
    ],
)
async def test_invalidate_access_token(
    populate: bool, email: str, iat: int
) -> None:
    assert populate
    loaders: Dataloaders = get_new_context()
    stakeholder = await loaders.stakeholder.load(email)
    assert stakeholder
    assert stakeholder.access_token is not None
    assert stakeholder.access_token.iat == iat
    result: dict[str, Any] = await get_result(
        user=email,
    )
    assert "errors" not in result
    assert "invalidateAccessToken" in result["data"]
    assert "success" in result["data"]["invalidateAccessToken"]
    assert result["data"]["invalidateAccessToken"]["success"]
    new_loader = get_new_context()
    new_stakeholder = await new_loader.stakeholder.load(email)
    assert new_stakeholder
    assert new_stakeholder.access_token is None
