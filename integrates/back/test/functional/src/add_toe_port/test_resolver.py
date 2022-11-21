# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from . import (
    get_result,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_toe_port")
@pytest.mark.parametrize(
    ["email", "address", "port", "root_id"],
    [
        [
            "admin@fluidattacks.com",
            "192.168.1.1",
            "8080",
            "83cadbdc-23f3-463a-9421-f50f8d0cb1e5",
        ],
        [
            "admin@fluidattacks.com",
            "192.168.1.1",
            "8081",
            "83cadbdc-23f3-463a-9421-f50f8d0cb1e6",
        ],
    ],
)
async def test_add_toe_port(
    populate: bool,
    email: str,
    address: str,
    port: str,
    root_id: str,
) -> None:
    assert populate
    group_name: str = "group1"
    result: Dict[str, Any] = await get_result(
        address=address,
        port=port,
        group_name=group_name,
        root_id=root_id,
        user=email,
    )
    assert "errors" not in result
    assert "success" in result["data"]["addToePort"]
    assert result["data"]["addToePort"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_toe_port")
@pytest.mark.parametrize(
    ["email", "address", "port", "root_id"],
    [
        [
            "admin@fluidattacks.com",
            "192.168.1.2",
            "8080",
            "7a9759ad-218a-4a98-9210-31dd78d61580",
        ],
    ],
)
async def test_add_toe_port_already_exists(
    populate: bool,
    email: str,
    address: str,
    port: str,
    root_id: str,
) -> None:
    assert populate
    group_name: str = "group1"
    result: Dict[str, Any] = await get_result(
        address=address,
        port=port,
        group_name=group_name,
        root_id=root_id,
        user=email,
    )
    assert "errors" in result
    assert (
        result["errors"][0]["message"] == "Exception - Toe port already exists"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_toe_port")
@pytest.mark.parametrize(
    ["email", "address", "port", "root_id"],
    [
        [
            "admin@fluidattacks.com",
            "192.168.1.1",
            "8080",
            "13cadbdc-23f3-463a-9421-f50f8d0cb1e5",
        ],
        [
            "admin@fluidattacks.com",
            "192.168.1.1",
            "8081",
            "13cadbdc-23f3-463a-9421-f50f8d0cb1e6",
        ],
    ],
)
async def test_add_toe_port_root_not_found(
    populate: bool,
    email: str,
    address: str,
    port: str,
    root_id: str,
) -> None:
    assert populate
    group_name: str = "group1"
    result: Dict[str, Any] = await get_result(
        address=address,
        port=port,
        group_name=group_name,
        root_id=root_id,
        user=email,
    )
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "Exception - Access denied or root not found"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_toe_port")
@pytest.mark.parametrize(
    ["email", "address", "port", "root_id"],
    [
        [
            "admin@fluidattacks.com",
            "192.168.1.2",
            "8080",
            "83cadbdc-23f3-463a-9421-f50f8d0cb1e5",
        ],
        [
            "admin@fluidattacks.com",
            "192.168.1.1",
            "8082",
            "83cadbdc-23f3-463a-9421-f50f8d0cb1e6",
        ],
    ],
)
async def test_add_toe_port_ip_and_port_do_not_exist(
    populate: bool,
    email: str,
    address: str,
    port: str,
    root_id: str,
) -> None:
    assert populate
    group_name: str = "group1"
    result: Dict[str, Any] = await get_result(
        address=address,
        port=port,
        group_name=group_name,
        root_id=root_id,
        user=email,
    )
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "Exception - The root does not have the IP and the port"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_toe_port")
@pytest.mark.parametrize(
    ["email", "address", "port", "root_id"],
    [
        [
            "user@gmail.com",
            "192.168.1.1",
            "8080",
            "83cadbdc-23f3-463a-9421-f50f8d0cb1e5",
        ],
    ],
)
async def test_add_toe_port_access_denied(
    populate: bool,
    email: str,
    address: str,
    port: str,
    root_id: str,
) -> None:
    assert populate
    group_name: str = "group1"
    result: Dict[str, Any] = await get_result(
        address=address,
        port=port,
        group_name=group_name,
        root_id=root_id,
        user=email,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
