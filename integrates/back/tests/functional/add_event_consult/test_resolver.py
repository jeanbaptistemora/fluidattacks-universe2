from . import (
    get_result,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_event_consult")
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
        ["reviewer@gmail.com"],
        ["group_manager@gmail.com"],
    ],
)
async def test_add_event_consult(populate: bool, email: str) -> None:
    assert populate
    event_id: str = "418900971"
    result: Dict[str, Any] = await get_result(
        user=email,
        event=event_id,
    )
    assert "errors" not in result
    assert "success" in result["data"]["addEventConsult"]
    assert result["data"]["addEventConsult"]
