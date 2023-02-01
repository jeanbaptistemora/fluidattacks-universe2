from . import (
    get_result,
)
from dataloaders import (
    get_new_context,
)
from db_model.roots.types import (
    IPRoot,
    RootRequest,
)
import pytest
from typing import (
    Any,
    cast,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_ip_root")
@pytest.mark.parametrize(
    ["email", "nickname", "address"],
    [
        [
            "admin@gmail.com",
            "test-nickname-1",
            "127.0.0.1",
        ],
        [
            "admin@fluidattacks.com",
            "test-nickname-2",
            "192.158.1.38",
        ],
    ],
)
async def test_add_ip_root(
    populate: bool,
    email: str,
    nickname: str,
    address: str,
) -> None:
    assert populate
    group_name: str = "group2"
    result: dict[str, Any] = await get_result(
        user=email,
        group=group_name,
        nickname=nickname,
        address=address,
    )
    assert "errors" not in result
    assert result["data"]["addIpRoot"]["success"]

    loaders = get_new_context()
    root_id = result["data"]["addIpRoot"]["rootId"]
    root = cast(
        IPRoot, await loaders.root.load(RootRequest(group_name, root_id))
    )
    assert root.state.nickname == nickname
    assert root.state.address == address


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_ip_root")
@pytest.mark.parametrize(
    ["email", "nickname", "address"],
    [
        [
            "admin@gmail.com",
            "test-nickname-1",
            "random_str",
        ],
    ],
)
async def test_add_ip_root_fail_1(
    populate: bool,
    email: str,
    nickname: str,
    address: str,
) -> None:
    assert populate
    group_name: str = "group2"
    result: dict[str, Any] = await get_result(
        user=email,
        group=group_name,
        nickname=nickname,
        address=address,
    )
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "Exception - Error value is not valid"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_ip_root")
@pytest.mark.parametrize(
    ["email", "nickname", "address"],
    [
        [
            "admin@gmail.com",
            "test_ip_1",
            "192.168.1.1",
        ],
    ],
)
async def test_add_ip_root_fail_2(
    populate: bool,
    email: str,
    nickname: str,
    address: str,
) -> None:
    assert populate
    group_name: str = "group2"
    result: dict[str, Any] = await get_result(
        user=email,
        group=group_name,
        nickname=nickname,
        address=address,
    )
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "Exception - Active root with the same Nickname already exists"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_ip_root")
@pytest.mark.parametrize(
    ["email", "nickname", "address"],
    [
        [
            "hacker@gmail.com",
            "test_nickname_1",
            "134.152.1.30",
        ],
        [
            "user@gmail.com",
            "test_nickname_2",
            "192.0.2.1",
        ],
        [
            "user_manager@fluidattacks.com",
            "test_nickname_3",
            "172.16.0.0",
        ],
    ],
)
async def test_add_ip_root_fail_3(
    populate: bool,
    email: str,
    nickname: str,
    address: str,
) -> None:
    assert populate
    group_name: str = "group1"
    result: dict[str, Any] = await get_result(
        user=email,
        group=group_name,
        nickname=nickname,
        address=address,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
