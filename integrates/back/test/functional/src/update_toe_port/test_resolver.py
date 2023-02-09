# pylint: disable=too-many-arguments
from . import (
    get_result,
)
from dataloaders import (
    get_new_context,
)
from db_model.toe_ports.types import (
    ToePortRequest,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_toe_port")
@pytest.mark.parametrize(
    ["email", "address", "port", "root_id", "be_present", "has_recent_attack"],
    [
        [
            "admin@fluidattacks.com",
            "192.168.1.1",
            "8080",
            "63298a73-9dff-46cf-b42d-9b2f01a56690",
            True,
            True,
        ],
        [
            "admin@fluidattacks.com",
            "192.168.1.1",
            "8081",
            "765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a",
            True,
            False,
        ],
    ],
)
async def test_update_toe_port(
    populate: bool,
    email: str,
    address: str,
    port: str,
    root_id: str,
    be_present: bool,
    has_recent_attack: bool,
) -> None:
    assert populate
    group_name: str = "group1"
    result: dict[str, Any] = await get_result(
        address=address,
        port=port,
        group_name=group_name,
        root_id=root_id,
        be_present=be_present,
        has_recent_attack=has_recent_attack,
        user=email,
    )
    assert "errors" not in result
    assert "success" in result["data"]["updateToePort"]
    assert result["data"]["updateToePort"]["success"]
    loaders = get_new_context()
    toe_port = await loaders.toe_port.load(
        ToePortRequest(
            group_name=group_name, address=address, port=port, root_id=root_id
        )
    )
    assert toe_port
    assert toe_port.state.be_present == be_present
    historic = await loaders.toe_port_historic_state.load(
        ToePortRequest(
            group_name=group_name, address=address, port=port, root_id=root_id
        )
    )
    assert len(historic) == 2


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_toe_port")
@pytest.mark.parametrize(
    ["email", "address", "port", "root_id", "be_present", "has_recent_attack"],
    [
        [
            "admin@fluidattacks.com",
            "192.168.1.1",
            "8080",
            "63298a73-9dff-46cf-b42d-9b2f01a56690",
            False,
            True,
        ],
        [
            "admin@fluidattacks.com",
            "192.168.1.1",
            "8082",
            "765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a",
            False,
            True,
        ],
    ],
)
async def test_update_toe_port_not_present(
    populate: bool,
    email: str,
    address: str,
    port: str,
    root_id: str,
    be_present: bool,
    has_recent_attack: bool,
) -> None:
    assert populate
    assert populate
    group_name: str = "group1"
    result: dict[str, Any] = await get_result(
        address=address,
        port=port,
        group_name=group_name,
        root_id=root_id,
        be_present=be_present,
        has_recent_attack=has_recent_attack,
        user=email,
    )
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "Exception - The toe port is not present"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_toe_port")
@pytest.mark.parametrize(
    ["email", "address", "port", "root_id", "be_present", "has_recent_attack"],
    [
        [
            "user@gmail.com",
            "192.168.1.1",
            "8080",
            "63298a73-9dff-46cf-b42d-9b2f01a56690",
            True,
            True,
        ],
    ],
)
async def test_update_toe_port_access_denied(
    populate: bool,
    email: str,
    address: str,
    port: str,
    root_id: str,
    be_present: bool,
    has_recent_attack: bool,
) -> None:
    assert populate
    assert populate
    group_name: str = "group1"
    result: dict[str, Any] = await get_result(
        address=address,
        port=port,
        group_name=group_name,
        root_id=root_id,
        be_present=be_present,
        has_recent_attack=has_recent_attack,
        user=email,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
