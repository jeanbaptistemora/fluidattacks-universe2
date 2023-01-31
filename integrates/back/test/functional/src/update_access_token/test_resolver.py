# pylint: disable=import-error
from . import (
    get_me_access_token,
    get_me_data,
    get_result,
)
from back.test.functional.src.invalidate_access_token import (
    get_result as invalidate_token,
)
from datetime import (
    datetime,
    timedelta,
)
import json
import pytest


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_access_token")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["hacker@gmail.com"],
        ["reattacker@gmail.com"],
        ["user@gmail.com"],
        ["user_manager@gmail.com"],
        ["vulnerability_manager@gmail.com"],
        ["resourcer@gmail.com"],
        ["customer_manager@fluidattacks.com"],
        ["reviewer@gmail.com"],
        ["service_forces@gmail.com"],
    ],
)
async def test_update_access_token(populate: bool, email: str) -> None:
    assert populate
    expiration_time: datetime = datetime.utcnow() + timedelta(weeks=8)
    ts_expiration_time: int = int(expiration_time.timestamp())
    result: dict = await get_result(
        user=email,
        expiration_time=ts_expiration_time,
    )
    assert "errors" not in result
    assert "updateAccessToken" in result["data"]
    assert "success" in result["data"]["updateAccessToken"]
    assert result["data"]["updateAccessToken"]["success"]

    session_jwt: str = result["data"]["updateAccessToken"]["sessionJwt"]
    me_token: dict = await get_me_access_token(user=email)
    assert "errors" not in me_token
    assert (
        json.loads(me_token["data"]["me"]["accessToken"])["lastAccessTokenUse"]
        is None
    )

    me_data: dict = await get_me_data(user=email, session_jwt=session_jwt)
    assert "errors" not in me_data
    assert len(me_data["data"]["me"]["permissions"]) > 0

    me_token = await get_me_access_token(user=email)
    assert "errors" not in me_token
    assert (
        json.loads(me_token["data"]["me"]["accessToken"])["hasAccessToken"]
        is True
    )
    assert (
        json.loads(me_token["data"]["me"]["accessToken"])["lastAccessTokenUse"]
        is not None
    )

    invalidate: dict = await invalidate_token(user=email)
    assert "errors" not in invalidate
    assert invalidate["data"]["invalidateAccessToken"]["success"]

    me_token = await get_me_access_token(user=email)
    assert "errors" not in me_token
    assert (
        json.loads(me_token["data"]["me"]["accessToken"])["hasAccessToken"]
        is False
    )
    assert (
        json.loads(me_token["data"]["me"]["accessToken"])["lastAccessTokenUse"]
        is None
    )
