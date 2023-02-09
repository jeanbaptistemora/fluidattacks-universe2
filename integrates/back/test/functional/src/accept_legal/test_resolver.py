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
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("accept_legal")
@pytest.mark.parametrize(
    ["email", "remember"],
    [
        ["admin@gmail.com", True],
        ["user@gmail.com", True],
        ["user_manager@gmail.com", True],
        ["hacker@gmail.com", True],
        ["reattacker@gmail.com", True],
        ["resourcer@gmail.com", True],
        ["reviewer@gmail.com", True],
        ["service_forces@gmail.com", True],
        ["customer_manager@gmail.com", True],
        ["vulnerability_manager@gmail.com", True],
    ],
)
async def test_accept_legal(
    populate: bool, email: str, remember: bool
) -> None:
    loaders: Dataloaders = get_new_context()
    stakeholder = await loaders.stakeholder.load(email)
    assert populate
    assert stakeholder
    assert stakeholder.legal_remember == remember
    result: Dict[str, Any] = await get_result(
        user=email,
    )
    new_loaders: Dataloaders = get_new_context()
    new_stakeholder = await new_loaders.stakeholder.load(email)
    assert new_stakeholder
    assert new_stakeholder.legal_remember is False

    assert "errors" not in result
    assert "acceptLegal" in result["data"]
    assert "success" in result["data"]["acceptLegal"]
    assert result["data"]["acceptLegal"]["success"]
