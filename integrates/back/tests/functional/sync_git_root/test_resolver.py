from . import (
    get_result,
)
from dataloaders import (
    get_new_context,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("sync_git_root")
@pytest.mark.parametrize(
    ["email", "root_id", "expected_status"],
    [
        ["admin@gmail.com", "e22a3a0d-05ac-4d13-8c81-7c829f8f96e3", "CLONING"],
        ["admin@gmail.com", "888648ed-a71c-42e5-b3e5-c3a370d26c68", "FAILED"],
    ],
)
async def test_sync_git_root(
    populate: bool, email: str, root_id: str, expected_status: str
) -> None:
    assert populate
    group_name: str = "group1"
    result: Dict[str, Any] = await get_result(
        user=email,
        group=group_name,
        root_id=root_id,
    )
    assert "errors" not in result
    assert result["data"]["syncGitRoot"]["success"]

    loaders = get_new_context()
    root = await loaders.root.load((group_name, root_id))
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
        [
            "admin@gmail.com",
            "58167a02-08c2-4cdf-a5e4-568398cbe7cb",
            "Exception - The root is not active",
        ],
        [
            "admin@gmail.com",
            "c75f9c2c-1984-49cf-bd3f-c628175a569c",
            "Exception - The root already has an active cloning process",
        ],
    ],
)
async def test_sync_git_root_error(
    populate: bool, email: str, root_id: str, expected_error: str
) -> None:
    assert populate
    group_name: str = "group1"
    result: Dict[str, Any] = await get_result(
        user=email,
        group=group_name,
        root_id=root_id,
    )
    assert result["errors"][0]["message"] == expected_error
