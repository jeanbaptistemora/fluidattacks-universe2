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
@pytest.mark.resolver_test_group("report")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["customeradmin@gmail.com"],
        ["hacker@gmail.com"],
    ],
)
async def test_get_report(populate: bool, email: str) -> None:
    assert populate
    group: str = "group1"
    result: Dict[str, Any] = await get_result(
        user=email,
        group_name=group,
    )
    assert "url" in result["data"]["report"]
    assert (
        result["data"]["report"]["url"]
        == f"""The report will be sent to {email} shortly"""
    )
