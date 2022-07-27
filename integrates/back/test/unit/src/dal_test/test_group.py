from db_model.group_access.types import (
    GroupAccessMetadataToUpdate,
)
from group_access.dal import (
    get_group_users,
    update_metadata,
)
import pytest

pytestmark = [
    pytest.mark.asyncio,
]


async def test_update_access() -> None:
    assert "unittest2@fluidattacks.com" in await get_group_users(
        "unittesting", True
    )
    await update_metadata(
        email="unittest2@fluidattacks.com",
        group_name="unittesting",
        metadata=GroupAccessMetadataToUpdate(
            has_access=False,
        ),
    )
    assert "unittest2@fluidattacks.com" in await get_group_users(
        "unittesting", False
    )
    await update_metadata(
        email="unittest2@fluidattacks.com",
        group_name="unittesting",
        metadata=GroupAccessMetadataToUpdate(
            has_access=True,
        ),
    )
    assert "unittest2@fluidattacks.com" in await get_group_users(
        "unittesting", True
    )
