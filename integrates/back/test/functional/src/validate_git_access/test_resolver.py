from . import (
    get_result,
)
import os
import pytest


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("validate_git_access")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
    ],
)
async def test_validate_git_access(populate: bool, email: str) -> None:
    assert populate
    group_name: str = "group1"
    key: str = os.environ["TEST_SSH_KEY"]
    url = "git@gitlab.com:fluidattacks/universe.git"
    result = await get_result(user=email, group=group_name, key=key, url=url)
    assert "errors" not in result
    assert result["data"]["validateGitAccess"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("validate_git_access")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
    ],
)
async def test_validate_git_access_fail(populate: bool, email: str) -> None:
    assert populate
    group_name: str = "group1"
    key: str = "VGVzdCBTU0gK"
    url = "git@gitlab.com:fluidattacks/test-universe-test-fail-functional.git"
    result = await get_result(user=email, group=group_name, key=key, url=url)
    assert (
        result["errors"][0]["message"]
        == "Exception - Git repository was not accessible with given"
        " credentials"
    )
