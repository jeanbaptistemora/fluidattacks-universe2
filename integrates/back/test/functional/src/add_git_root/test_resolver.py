# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# pylint: disable=import-error
from . import (
    get_result,
)
from back.test.functional.src.organization import (
    get_result as get_organization,
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
@pytest.mark.resolver_test_group("add_git_root_s3")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
    ],
)
async def test_add_git_root(populate: bool, email: str) -> None:
    assert populate
    group_name: str = "group1"
    org_id: str = "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db"

    organization: dict = await get_organization(user=email, org=org_id)
    assert (
        len(
            organization["data"]["organization"][
                "integrationRepositoriesConnection"
            ]["edges"]
        )
        == 1
    )

    result: Dict[str, Any] = await get_result(
        user=email,
        group=group_name,
    )
    assert "errors" not in result
    assert result["data"]["addGitRoot"]["success"]

    loaders = get_new_context()
    root_id = result["data"]["addGitRoot"]["rootId"]
    root = await loaders.root.load((group_name, root_id))
    assert root.cloning.status.value == "QUEUED"
    assert root.cloning.reason == "Cloning queued..."

    organization = await get_organization(user=email, org=org_id)
    assert (
        len(
            organization["data"]["organization"][
                "integrationRepositoriesConnection"
            ]["edges"]
        )
        == 0
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_git_root_s3")
@pytest.mark.parametrize(
    ["email"],
    [
        ["user@gmail.com"],
        ["user_manager@gmail.com"],
        ["resourcer@gmail.com"],
        ["customer_manager@fluidattacks.com"],
    ],
)
async def test_add_git_root_fail_1(populate: bool, email: str) -> None:
    assert populate
    group_name: str = "group1"
    result: Dict[str, Any] = await get_result(
        user=email,
        group=group_name,
    )
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "Exception - Active root with the same Nickname already exists"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_git_root_s3")
@pytest.mark.parametrize(
    ["email"],
    [
        ["hacker@gmail.com"],
        ["reattacker@gmail.com"],
        ["vulnerability_manager@gmail.com"],
    ],
)
async def test_add_git_root_fail_2(populate: bool, email: str) -> None:
    assert populate
    group_name: str = "group1"
    result: Dict[str, Any] = await get_result(
        user=email,
        group=group_name,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
