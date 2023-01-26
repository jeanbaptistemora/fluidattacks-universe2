from . import (
    get_result,
)
from dataloaders import (
    get_new_context,
)
from db_model.roots.types import (
    RootRequest,
    URLRoot,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_url_root")
@pytest.mark.parametrize(
    ["email", "nickname", "query", "url"],
    [
        [
            "admin@gmail.com",
            "test-nickname-1",
            "=test",
            "https://test.com",
        ],
        [
            "admin@gmail.com",
            "test-nickname-2",
            "test=test2",
            "https://test2.com",
        ],
    ],
)
async def test_add_url_root(
    populate: bool,
    email: str,
    nickname: str,
    query: str,
    url: str,
) -> None:
    assert populate
    group_name: str = "group2"
    result: dict[str, Any] = await get_result(
        user=email,
        group=group_name,
        nickname=nickname,
        url=f"{url}?{query}",
    )
    assert "errors" not in result
    assert result["data"]["addUrlRoot"]["success"]

    loaders = get_new_context()
    root_id = result["data"]["addUrlRoot"]["rootId"]
    root: URLRoot = await loaders.root.load(RootRequest(group_name, root_id))
    assert root.state.nickname == nickname
    assert root.state.query == query


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_url_root")
@pytest.mark.parametrize(
    ["email", "nickname", "query", "url"],
    [
        [
            "admin@gmail.com",
            "test-nickname-1",
            "=test",
            "https://test.com",
        ],
    ],
)
async def test_add_url_root_fail_1(
    populate: bool,
    email: str,
    nickname: str,
    query: str,
    url: str,
) -> None:
    assert populate
    group_name: str = "group2"
    result: dict[str, Any] = await get_result(
        user=email,
        group=group_name,
        nickname=nickname,
        url=f"{url}?{query}",
    )
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "Exception - Active root with the same Nickname already exists"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_url_root")
@pytest.mark.parametrize(
    ["email"],
    [
        ["hacker@gmail.com"],
        ["reattacker@gmail.com"],
        ["vulnerability_manager@gmail.com"],
    ],
)
async def test_add_url_root_fail_2(populate: bool, email: str) -> None:
    assert populate
    group_name: str = "group1"
    result: dict[str, Any] = await get_result(
        user=email,
        group=group_name,
        nickname="nickname",
        url="url",
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
