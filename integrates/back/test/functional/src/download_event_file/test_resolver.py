from . import (
    get_result,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("download_event_file")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["hacker@gmail.com"],
        ["reattacker@gmail.com"],
        ["user@gmail.com"],
        ["user_manager@gmail.com"],
        ["vulnerability_manager@gmail.com"],
        ["executive@gmail.com"],
        ["resourcer@gmail.com"],
        ["reviewer@gmail.com"],
        ["customer_manager@fluidattacks.com"],
    ],
)
async def test_download_event_file(populate: bool, email: str) -> None:
    assert populate
    event_id: str = "418900971"
    result: Dict[str, Any] = await get_result(user=email, event=event_id)
    assert "errors" not in result
    assert "success" in result["data"]["downloadEventFile"]
    assert result["data"]["downloadEventFile"]
    assert "url" in result["data"]["downloadEventFile"]
