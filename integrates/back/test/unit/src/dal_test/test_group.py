from dataloaders import (
    get_new_context,
)
from db_model.group_access.types import (
    GroupAccessMetadataToUpdate,
)
from group_access.dal import (
    update_metadata,
)
from group_access.domain import (
    get_group_stakeholders_emails,
)
import pytest

pytestmark = [
    pytest.mark.asyncio,
]


async def test_update_access() -> None:
    assert "unittest2@fluidattacks.com" in await get_group_stakeholders_emails(
        get_new_context(), "unittesting", True
    )
    await update_metadata(
        email="unittest2@fluidattacks.com",
        group_name="unittesting",
        metadata=GroupAccessMetadataToUpdate(
            has_access=False,
        ),
    )
    assert "unittest2@fluidattacks.com" in await get_group_stakeholders_emails(
        get_new_context(), "unittesting", False
    )
    await update_metadata(
        email="unittest2@fluidattacks.com",
        group_name="unittesting",
        metadata=GroupAccessMetadataToUpdate(
            has_access=True,
        ),
    )
    assert "unittest2@fluidattacks.com" in await get_group_stakeholders_emails(
        get_new_context(), "unittesting", True
    )
