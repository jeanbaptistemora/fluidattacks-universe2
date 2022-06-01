from . import (
    get_result_add,
    get_result_remove,
)
from dataloaders import (
    get_new_context,
)
from db_model.roots.types import (
    GitRoot,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_git_environments")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
    ],
)
async def test_add_git_environments(populate: bool, email: str) -> None:
    assert populate
    group_name: str = "group1"
    root_id: str = "88637616-41d4-4242-854a-db8ff7fe1ab6"
    env_urls = ["https://nice-env.com", "https://nice-helper-site.co.uk"]

    loaders = get_new_context()
    root: GitRoot = await loaders.root.load((group_name, root_id))
    assert root.state.environment_urls == []

    result: Dict[str, Any] = await get_result_add(
        user=email,
        group=group_name,
        env_urls=env_urls,
        root_id=root_id,
    )
    assert "errors" not in result
    assert result["data"]["updateGitEnvironments"]["success"]

    loaders.root.clear_all()
    changed_root: GitRoot = await loaders.root.load((group_name, root_id))
    assert changed_root.state.environment_urls == env_urls


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_git_environments")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
    ],
)
async def test_remove_git_environments(populate: bool, email: str) -> None:
    assert populate
    group_name: str = "group1"
    root_id: str = "88637616-41d4-4242-854a-db8ff7fe1ab7"
    env_urls = ["https://nice-env.net", "https://mistaken-site.ru"]

    loaders = get_new_context()
    root: GitRoot = await loaders.root.load((group_name, root_id))
    assert root.state.environment_urls == env_urls

    result: Dict[str, Any] = await get_result_remove(
        user=email,
        group=group_name,
        env_urls=[env_urls[0]],
        other="",
        reason="REGISTERED_BY_MISTAKE",
        root_id=root_id,
    )
    assert "errors" not in result
    assert result["data"]["updateGitEnvironments"]["success"]

    loaders.root.clear_all()
    changed_root: GitRoot = await loaders.root.load((group_name, root_id))
    assert changed_root.state.environment_urls == [env_urls[0]]
