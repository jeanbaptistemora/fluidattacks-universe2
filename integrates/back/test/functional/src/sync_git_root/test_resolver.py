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
@pytest.mark.resolver_test_group("sync_git_root")
@pytest.mark.parametrize(
    ["email", "root_id", "expected_status"],
    [
        ["admin@gmail.com", "e22a3a0d-05ac-4d13-8c81-7c829f8f96e3", "QUEUED"],
    ],
)
async def test_sync_git_root(
    populate: bool, email: str, root_id: str, expected_status: str
) -> None:
    assert populate
    group_name: str = "group1"
    result: dict[str, Any] = await get_result(
        user=email,
        group=group_name,
        root_id=root_id,
    )
    assert "errors" not in result
    assert result["data"]["syncGitRoot"]["success"]

    loaders = get_new_context()
    root = cast(
        GitRoot, await loaders.root.load(RootRequest(group_name, root_id))
    )
    assert root.cloning.status.value == expected_status


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("sync_git_root")
@pytest.mark.parametrize(
    ["email", "root_id", "expected_error"],
    [
        [
            "admin@gmail.com",
            "3626aca5-099c-42b9-aa25-d8c6e0aab98f",
            "Exception - Access denied or credential not found",
        ],
    ],
)
async def test_sync_git_root_error(
    populate: bool, email: str, root_id: str, expected_error: str
) -> None:
    assert populate
    group_name: str = "group1"
    result: dict[str, Any] = await get_result(
        user=email,
        group=group_name,
        root_id=root_id,
    )
    assert result["errors"][0]["message"] == expected_error
