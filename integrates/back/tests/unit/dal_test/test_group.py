from group_access.dal import (
    get_group_users,
    update as update_access,
)
from group_access.domain import (
    list_internal_owners,
)
import pytest

pytestmark = [
    pytest.mark.asyncio,
]


async def test_list_internal_managers() -> None:
    assert await list_internal_owners("oneshottest") == []
    assert await list_internal_owners("unittesting") == [
        "unittest2@fluidattacks.com",
        "customer_manager@fluidattacks.com",
    ]


async def test_update_access() -> None:
    assert "unittest2@fluidattacks.com" in await get_group_users(
        "unittesting", True
    )
    assert await update_access(
        "unittest2@fluidattacks.com", "unittesting", {"has_access": False}
    )
    assert "unittest2@fluidattacks.com" in await get_group_users(
        "unittesting", False
    )
    assert await update_access(
        "unittest2@fluidattacks.com", "unittesting", {"has_access": True}
    )
    assert "unittest2@fluidattacks.com" in await get_group_users(
        "unittesting", True
    )
