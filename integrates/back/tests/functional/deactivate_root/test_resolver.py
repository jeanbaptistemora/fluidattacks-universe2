# Standard
import pytest
from typing import Optional

# Local
from . import query


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("deactivate_root")
@pytest.mark.parametrize(
    ("root_id",),
    (
        ("63298a73-9dff-46cf-b42d-9b2f01a56690",),
        ("83cadbdc-23f3-463a-9421-f50f8d0cb1e5",),
        ("eee8b331-98b9-4e32-a3c7-ec22bd244ae8",),
    ),
)
@pytest.mark.parametrize(
    ("reason", "new_root_id"),
    (
        ("MOVED_TO_ANOTHER_ROOT", "00000000-0000-0000-0000-000000000000"),
        ("OUT_OF_SCOPE", None),
        ("REGISTERED_BY_MISTAKE", None),
    ),
)
async def test_deactivate_root(
    populate: bool, root_id: str, reason: str, new_root_id: Optional[str]
):
    assert populate
    result = await query(
        email="admin@gmail.com",
        group_name="group1",
        id=root_id,
        new_root_id=new_root_id,
        reason=reason,
    )
    assert "errors" not in result
    assert result["data"]["deactivateRoot"]["success"]
