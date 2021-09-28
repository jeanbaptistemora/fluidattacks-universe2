from . import (
    get_result,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("me")
@pytest.mark.parametrize(
    ("email", "role", "permissions"),
    (
        ("admin@gmail.com", "admin", 13),
        ("customer@gmail.com", "customer", 1),
        ("customeradmin@gmail.com", "customeradmin", 0),
        ("executive@gmail.com", "executive", 0),
        ("hacker@gmail.com", "hacker", 1),
        ("reattacker@gmail.com", "reattacker", 0),
        ("resourcer@gmail.com", "resourcer", 0),
        ("reviewer@gmail.com", "reviewer", 0),
        ("service_forces@gmail.com", "service_forces", 0),
        ("system_owner@gmail.com", "system_owner", 0),
    ),
)
async def test_get_me(
    populate: bool, email: str, role: str, permissions: int
) -> None:
    assert populate
    org_name: str = "orgtest"
    organization: str = "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db"
    result: Dict[str, Any] = await get_result(
        user=email,
        org_id=organization,
    )
    assert "errors" not in result
    assert '{"hasAccessToken": false' in result["data"]["me"]["accessToken"]
    assert result["data"]["me"]["callerOrigin"] == "API"
    assert not result["data"]["me"]["isConcurrentSession"]
    assert result["data"]["me"]["organizations"] == [{"name": org_name}]
    assert len(result["data"]["me"]["permissions"]) == permissions
    assert not result["data"]["me"]["remember"]
    assert result["data"]["me"]["role"] == role
    assert result["data"]["me"]["subscriptionsToEntityReport"] == []
    assert result["data"]["me"]["tags"] == []
    assert result["data"]["me"]["__typename"] == "Me"
