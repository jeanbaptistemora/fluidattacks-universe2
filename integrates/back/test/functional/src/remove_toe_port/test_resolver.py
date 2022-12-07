from custom_exceptions import (
    ToePortNotFound,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model import (
    toe_ports as toe_ports_model,
)
from db_model.toe_ports.types import (
    GroupToePortsRequest,
    ToePort,
    ToePortRequest,
    ToePortState,
)
import pytest


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("remove_toe_port")
@pytest.mark.parametrize(
    [
        "address",
        "port",
        "root_id",
    ],
    [
        [
            "192.168.1.1",
            "8080",
            "63298a73-9dff-46cf-b42d-9b2f01a56690",
        ],
        [
            "192.168.1.1",
            "8081",
            "765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a",
        ],
    ],
)
async def test_remove_toe_port(
    populate: bool,
    address: str,
    port: str,
    root_id: str,
) -> None:
    assert populate
    group_name: str = "group1"
    loaders: Dataloaders = get_new_context()
    request = ToePortRequest(
        group_name=group_name, address=address, port=port, root_id=root_id
    )
    toe_port: ToePort = await loaders.toe_port.load(request)
    assert toe_port.address == address
    historic: tuple[
        ToePortState, ...
    ] = await loaders.toe_port_historic_state.load(request)
    assert len(historic) == 1
    await toe_ports_model.remove(
        group_name=group_name, address=address, port=port, root_id=root_id
    )
    loaders.toe_port.clear(request)
    loaders.toe_port_historic_state.clear(request)
    with pytest.raises(ToePortNotFound):
        await loaders.toe_port.load(request)
    historic = await loaders.toe_port_historic_state.load(request)
    assert len(historic) == 0


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("remove_toe_port")
async def test_remove_group_toe_ports(
    populate: bool,
) -> None:
    assert populate
    group_name: str = "group2"
    loaders: Dataloaders = get_new_context()
    group_request = GroupToePortsRequest(group_name=group_name)
    toe_ports: tuple[ToePort, ...] = await loaders.group_toe_ports.load_nodes(
        group_request
    )
    assert len(toe_ports) == 3
    request = ToePortRequest(
        group_name=group_name,
        address=toe_ports[1].address,
        port=toe_ports[1].port,
        root_id=toe_ports[1].root_id,
    )
    historic: tuple[
        ToePortState, ...
    ] = await loaders.toe_port_historic_state.load(request)
    assert len(historic) == 1
    await toe_ports_model.remove_group_toe_ports(group_name=group_name)
    loaders.group_toe_ports.clear(group_request)
    loaders.toe_port_historic_state.clear(request)
    toe_ports = await loaders.group_toe_ports.load_nodes(group_request)
    assert len(toe_ports) == 0
    historic = await loaders.toe_port_historic_state.load(request)
    assert len(historic) == 0
