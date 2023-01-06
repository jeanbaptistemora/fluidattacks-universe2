# pylint: disable=import-error
from . import (
    get_result_add,
    get_result_remove,
    mutation_add,
    mutation_remove,
)
from back.test.functional.src.add_toe_input import (
    get_result,
)
from contextlib import (
    suppress,
)
from custom_exceptions import (
    InvalidBePresentFilterCursor,
    InvalidParameter,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.roots.types import (
    GitRoot,
)
from db_model.toe_inputs.types import (
    RootToeInputsRequest,
    ToeInput,
)
import hashlib
import pytest
from typing import (
    Any,
    Dict,
)


async def _get_root_toe_inputs(
    be_present: bool,
    group_name: str,
    root_id: str,
) -> tuple[ToeInput, ...]:
    loaders: Dataloaders = get_new_context()

    root_toe_inputs = loaders.root_toe_inputs.load_nodes(
        RootToeInputsRequest(
            be_present=be_present,
            group_name=group_name,
            root_id=root_id,
        )
    )
    if root_toe_inputs:
        return await root_toe_inputs
    raise InvalidBePresentFilterCursor()


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

    with suppress(InvalidParameter):
        # No reason for deletion
        await get_result_remove(
            user=email,
            group=group_name,
            env_urls=[env_urls[0]],
            other="",
            reason="",
            root_id=root_id,
        )
        # Not specifying other when pointing it out as the reason
        await get_result_remove(
            user=email,
            group=group_name,
            env_urls=[env_urls[0]],
            other="",
            reason="OTHER",
            root_id=root_id,
        )

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


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_git_environments")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
    ],
)
async def test_add_git_environment_url(populate: bool, email: str) -> None:
    assert populate
    group_name: str = "group1"
    root_id: str = "88637616-41d4-4242-854a-db8ff7fe1ab6"
    env_urls = "https://nice-env-test.com"

    loaders = get_new_context()
    assert len(await loaders.root_environment_urls.load((root_id))) == 2

    result: Dict[str, Any] = await mutation_add(
        user=email,
        group_name=group_name,
        url=env_urls,
        url_type="URL",
        root_id=root_id,
    )
    assert "errors" not in result
    assert result["data"]["addGitEnvironmentUrl"]["success"]

    loaders.root_environment_urls.clear_all()
    assert len(await loaders.root_environment_urls.load((root_id))) == 3
    assert len(await _get_root_toe_inputs(True, group_name, root_id)) == 0

    result_toe: Dict[str, Any] = await get_result(
        component=env_urls,
        entry_point="idBtn",
        group_name=group_name,
        root_id=root_id,
        user="admin@fluidattacks.com",
    )
    assert "errors" not in result_toe
    assert result_toe["data"]["addToeInput"]["success"]

    loaders.root_toe_inputs.clear_all()
    assert len(await _get_root_toe_inputs(False, group_name, root_id)) == 0
    assert len(await _get_root_toe_inputs(True, group_name, root_id)) == 1


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_git_environments")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
    ],
)
async def test_remove_git_environment_url(populate: bool, email: str) -> None:
    assert populate
    group_name: str = "group1"
    root_id: str = "88637616-41d4-4242-854a-db8ff7fe1ab6"
    env_urls = "https://nice-env-test.com"

    loaders = get_new_context()
    assert len(await loaders.root_environment_urls.load((root_id))) == 3

    result: Dict[str, Any] = await mutation_remove(
        group_name=group_name,
        root_id=root_id,
        url_id=hashlib.sha1(env_urls.encode()).hexdigest(),
        user=email,
    )
    assert "errors" not in result
    assert result["data"]["removeEnvironmentUrl"]["success"]

    loaders.root_environment_urls.clear_all()
    loaders.root_toe_inputs.clear_all()
    assert len(await _get_root_toe_inputs(True, group_name, root_id)) == 1
    assert len(await loaders.root_environment_urls.load((root_id))) == 2
    assert len(await _get_root_toe_inputs(False, group_name, root_id)) == 0
