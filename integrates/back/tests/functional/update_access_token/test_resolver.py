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
@pytest.mark.resolver_test_group("update_access_token")
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
    ],
)
async def test_update_access_token(populate: bool, email: str) -> None:
    assert populate
    expiration_time: Any = datetime.utcnow() + timedelta(weeks=8)
    ts_expiration_time: int = int(expiration_time.timestamp())
    result: Dict[str, Any] = await get_result(
        user=email,
        expiration_time=ts_expiration_time,
    )
    assert "errors" not in result
    assert result["data"]["updateAccessToken"]["success"]
