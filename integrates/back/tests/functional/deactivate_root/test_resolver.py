from . import (
    get_result,
)
import pytest
from typing import (
    Optional,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("deactivate_root")
@pytest.mark.parametrize(
    ("group_name", "root_id"),
    (
        (
            "group1",
            "63298a73-9dff-46cf-b42d-9b2f01a56690",
        ),
        (
            "group2",
            "83cadbdc-23f3-463a-9421-f50f8d0cb1e5",
        ),
        (
            "group2",
            "eee8b331-98b9-4e32-a3c7-ec22bd244ae8",
        ),
    ),
)
@pytest.mark.parametrize(
    ("reason", "other"),
    (
        ("OTHER", "custom reason"),
        ("OUT_OF_SCOPE", None),
        ("REGISTERED_BY_MISTAKE", None),
    ),
)
async def test_deactivate_root(
    populate: bool,
    group_name: str,
    root_id: str,
    reason: str,
    other: Optional[str],
) -> None:
    # pylint: disable=unsubscriptable-object
    assert populate
    result = await get_result(
        email="admin@gmail.com",
        group_name=group_name,
        identifier=root_id,
        reason=reason,
        other=other,
    )
    assert "errors" not in result
    assert result["data"]["deactivateRoot"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("deactivate_root")
@pytest.mark.parametrize(
    ("group_name", "root_id"),
    (
        (
            "group2",
            "702b81b3-d741-4699-9173-ecbc30bfb0cb",
        ),
        (
            "group1",
            "44db9bee-c97d-4161-98c6-f124d7dc9a41",
        ),
        (
            "group1",
            "bd4e5e66-da26-4274-87ed-17de7c3bc2f1",
        ),
    ),
)
async def test_deactivate_root_fail(
    populate: bool,
    group_name: str,
    root_id: str,
) -> None:
    assert populate
    result = await get_result(
        email="admin@gmail.com",
        group_name=group_name,
        identifier=root_id,
        reason="REGISTERED_BY_MISTAKE",
        other=None,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
