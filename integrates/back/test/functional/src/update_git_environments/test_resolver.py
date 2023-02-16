from . import (
    get_git_root,
    get_result_add,
    get_result_remove,
    mutation_add,
    mutation_add_secret,
    mutation_remove,
    mutation_remove_secret,
)
from back.test.functional.src.add_toe_input import (  # noqa: E501 pylint: disable=import-error
    get_result,
)
from contextlib import (
    suppress,
)
from custom_exceptions import (
    InvalidParameter,
)
from dataloaders import (
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model.roots.types import (
    GitRoot,
    RootEnvironmentUrlType,
    RootRequest,
    Secret,
)
from db_model.toe_inputs.types import (
    RootToeInputsRequest,
    ToeInput,
)
import hashlib
import pytest
from typing import (
    Any,
    cast,
)


async def _get_root_toe_inputs(
    be_present: bool,
    group_name: str,
    root_id: str,
) -> list[ToeInput]:
    loaders = get_new_context()
    return await loaders.root_toe_inputs.load_nodes(
        RootToeInputsRequest(
            be_present=be_present,
            group_name=group_name,
            root_id=root_id,
        )
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
    env_urls = ["https://nice-helper-site.co.uk", "https://nice-env.com"]

    loaders = get_new_context()
    root = cast(
        GitRoot, await loaders.root.load(RootRequest(group_name, root_id))
    )
    assert root.state.modified_date == datetime.fromisoformat(
        "2022-02-10T14:58:10+00:00"
    )
    result_group: dict = await get_git_root(
        user=email,
        group="group1",
        root_id=root_id,
    )
    assert "errors" not in result_group
    assert result_group["data"]["root"] == {
        "environmentUrls": [],
        "gitEnvironmentUrls": [],
        "id": "88637616-41d4-4242-854a-db8ff7fe1ab6",
    }

    result: dict[str, Any] = await get_result_add(
        user=email,
        group=group_name,
        env_urls=env_urls,
        root_id=root_id,
    )
    assert "errors" not in result
    assert result["data"]["updateGitEnvironments"]["success"]

    loaders.root.clear_all()
    changed_root = cast(
        GitRoot, await loaders.root.load(RootRequest(group_name, root_id))
    )
    assert changed_root.state.modified_date.date() == datetime.now().date()
    result_group = await get_git_root(
        user=email,
        group="group1",
        root_id=root_id,
    )
    assert "errors" not in result_group
    assert sorted(result_group["data"]["root"]["environmentUrls"]) == sorted(
        env_urls
    )
    assert sorted(
        result_group["data"]["root"]["gitEnvironmentUrls"],
        key=lambda x: x["url"],
    ) == sorted(
        [
            {"url": url, "urlType": RootEnvironmentUrlType.URL}
            for url in env_urls
        ],
        key=lambda x: x["url"],
    )
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
    root = cast(
        GitRoot, await loaders.root.load(RootRequest(group_name, root_id))
    )
    result_group: dict = await get_git_root(
        user=email,
        group="group1",
        root_id=root_id,
    )
    assert "errors" not in result_group
    assert sorted(result_group["data"]["root"]["environmentUrls"]) == sorted(
        env_urls
    )
    assert sorted(
        result_group["data"]["root"]["gitEnvironmentUrls"],
        key=lambda x: x["url"],
    ) == sorted(
        [
            {"url": url, "urlType": RootEnvironmentUrlType.URL}
            for url in env_urls
        ],
        key=lambda x: x["url"],
    )
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

    result: dict[str, Any] = await get_result_remove(
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
    changed_root = cast(
        GitRoot, await loaders.root.load(RootRequest(group_name, root_id))
    )
    result_group = await get_git_root(
        user=email,
        group="group1",
        root_id=root_id,
    )
    assert "errors" not in result_group
    assert result_group["data"]["root"] == {
        "environmentUrls": [env_urls[0]],
        "gitEnvironmentUrls": [
            {"url": url, "urlType": RootEnvironmentUrlType.URL}
            for url in [env_urls[0]]
        ],
        "id": "88637616-41d4-4242-854a-db8ff7fe1ab7",
    }
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
    assert len(await loaders.root_environment_urls.load(root_id)) == 2

    result: dict[str, Any] = await mutation_add(
        user=email,
        group_name=group_name,
        url=env_urls,
        url_type="URL",
        root_id=root_id,
    )
    assert "errors" not in result
    assert result["data"]["addGitEnvironmentUrl"]["success"]

    loaders.root_environment_urls.clear_all()
    assert len(await loaders.root_environment_urls.load(root_id)) == 3
    assert len(await _get_root_toe_inputs(True, group_name, root_id)) == 0

    result_toe: dict[str, Any] = await get_result(
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
async def test_add_git_environment_url_secret(
    populate: bool, email: str
) -> None:
    assert populate
    group_name: str = "group1"
    url_id: str = "e6118eb4696e04e882362cf2159baf240687256f"

    result: dict[str, Any] = await mutation_add_secret(
        user=email,
        group_name=group_name,
        key="user",
        url_id=url_id,
        value="integrates_test",
    )
    assert "errors" not in result
    assert result["data"]["addGitEnvironmentSecret"]["success"]

    loaders = get_new_context()
    secrets = await loaders.environment_secrets.load(url_id)
    assert len(secrets) > 0

    secret: Secret = secrets[0]
    assert secret.key == "user"
    assert secret.value == "integrates_test"


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
    assert len(await loaders.root_environment_urls.load(root_id)) == 3

    result: dict[str, Any] = await mutation_remove(
        group_name=group_name,
        root_id=root_id,
        url_id=hashlib.sha1(env_urls.encode()).hexdigest(),
        user=email,
    )
    assert "errors" not in result
    assert result["data"]["removeEnvironmentUrl"]["success"]

    loaders.root_environment_urls.clear_all()
    loaders.root_toe_inputs.clear_all()
    assert len(await _get_root_toe_inputs(True, group_name, root_id)) == 0
    assert len(await loaders.root_environment_urls.load(root_id)) == 2
    assert len(await _get_root_toe_inputs(False, group_name, root_id)) == 1


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_git_environments")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
    ],
)
async def test_remove_environment_url_secret(
    populate: bool, email: str
) -> None:
    assert populate
    group_name: str = "group1"
    url_id: str = "e6118eb4696e04e882362cf2159baf240687256f"

    result: dict[str, Any] = await mutation_remove_secret(
        user=email,
        group_name=group_name,
        key="user",
        url_id=url_id,
    )
    assert "errors" not in result
    assert result["data"]["removeEnvironmentUrlSecret"]["success"]

    loaders = get_new_context()
    secrets = await loaders.environment_secrets.load(url_id)
    assert len(secrets) == 0
