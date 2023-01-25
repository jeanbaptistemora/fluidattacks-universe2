from . import (
    get_result,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.toe_ports.types import (
    ToePort,
    ToePortRequest,
)
import pytest
from typing import (
    Any,
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
    result: dict[str, Any] = await get_result(
        address=address,
        port=port,
        group_name=group_name,
        root_id=root_id,
        user=email,
    )
    assert "errors" not in result
    assert "success" in result["data"]["addToePort"]
    assert result["data"]["addToePort"]["success"]
    loaders: Dataloaders = get_new_context()
    toe_port: ToePort = await loaders.toe_port.load(
        ToePortRequest(
            group_name=group_name, address=address, port=port, root_id=root_id
        )
    )
    assert toe_port.address == address
    assert toe_port.port == port
    assert toe_port.root_id == root_id
    assert toe_port.seen_first_time_by == email
    historic = await loaders.toe_port_historic_state.load(
        ToePortRequest(
            group_name=group_name, address=address, port=port, root_id=root_id
        )
    )
    assert len(historic) == 1


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
    result: dict[str, Any] = await get_result(
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
    result: dict[str, Any] = await get_result(
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
            "192.168.1.4",
            "8080",
            "83cadbdc-23f3-463a-9421-f50f8d0cb1e5",
        ],
        [
            "admin@fluidattacks.com",
            "192.168.1.5",
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
    result: dict[str, Any] = await get_result(
        address=address,
        port=port,
        group_name=group_name,
        root_id=root_id,
        user=email,
    )
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "Exception - The root does not have the IP address"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_toe_port")
@pytest.mark.parametrize(
    ["email", "address", "port", "root_id"],
    [
        [
            "admin@fluidattacks.com",
            "192.168.1.1",
            "65538",
            "83cadbdc-23f3-463a-9421-f50f8d0cb1e5",
        ],
    ],
)
async def test_add_toe_port_invalid_port(
    populate: bool,
    email: str,
    address: str,
    port: str,
    root_id: str,
) -> None:
    assert populate
    group_name: str = "group1"
    result: dict[str, Any] = await get_result(
        address=address,
        port=port,
        group_name=group_name,
        root_id=root_id,
        user=email,
    )
    assert "errors" in result
    assert "Exception - Error in port value" in result["errors"][0]["message"]


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
    result: dict[str, Any] = await get_result(
        address=address,
        port=port,
        group_name=group_name,
        root_id=root_id,
        user=email,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
