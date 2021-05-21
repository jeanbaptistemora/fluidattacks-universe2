# Standard libraries
import pytest
from typing import (
    Any,
    Dict,
)
from datetime import datetime, timedelta

# Local libraries
from . import query


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_access_token")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["analyst@gmail.com"],
        ["closer@gmail.com"],
        ["customer@gmail.com"],
    ],
)
async def test_update_access_token(populate: bool, email: str):
    assert populate
    expiration_time: Any = datetime.utcnow() + timedelta(weeks=8)
    ts_expiration_time: int = int(expiration_time.timestamp())
    result: Dict[str, Any] = await query(
        user=email,
        expiration_time=ts_expiration_time,
    )
    assert "errors" not in result
    assert result["data"]["updateAccessToken"]["success"]
