from . import (
    get_result,
)
from dataloaders import (
    get_new_context,
)
from db_model.roots.types import (
    GitRoot,
    RootRequest,
)
import pytest
from typing import (
    Any,
    cast,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_root_cloning_status")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
    ],
)
async def test_update_root_cloning_status(populate: bool, email: str) -> None:
    assert populate
    root_id: str = "765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a"
    group_name: str = "group2"
    loaders = get_new_context()
    result: dict[str, Any] = await get_result(
        user=email,
        group=group_name,
        root_id=root_id,
    )

    assert "errors" not in result
    assert "success" in result["data"]["updateRootCloningStatus"]
    assert result["data"]["updateRootCloningStatus"]["success"]

    root = cast(
        GitRoot, await loaders.root.load(RootRequest(group_name, root_id))
    )
    assert root.cloning.status == "OK"


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_root_cloning_status")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
    ],
)
async def test_update_root_cloning_status_fail_1(
    populate: bool,
    email: str,
) -> None:
    assert populate
    root_id: str = "be09edb7-cd5c-47ed-bee4-97c645acdce8"
    group_name: str = "group2"
    result: dict[str, Any] = await get_result(
        user=email,
        group=group_name,
        root_id=root_id,
    )

    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "Exception - Access denied or root not found"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_root_cloning_status")
@pytest.mark.parametrize(
    ["email"],
    [
        ["hacker@gmail.com"],
        ["user@gmail.com"],
        ["vulnerability_manager@fluidattacks.com"],
    ],
)
async def test_update_root_cloning_status_fail_2(
    populate: bool,
    email: str,
) -> None:
    assert populate
    root_id: str = "4039d098-ffc5-4984-8ed3-eb17bca98e199"
    group_name: str = "group2"
    result: dict[str, Any] = await get_result(
        user=email,
        group=group_name,
        root_id=root_id,
    )

    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
