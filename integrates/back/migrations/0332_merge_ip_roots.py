# pylint: disable=invalid-name
"""
Merge ip roots with the same address

Execution Time:    2022-12-15 at 18:44:17 UTC
Finalization Time: 2022-12-15 at 18:48:06 UTC
"""
from aioextensions import (
    collect,
    run,
)
import contextlib
import csv
from custom_exceptions import (
    RepeatedToeInput,
    RepeatedToePort,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model import (
    events as events_model,
    roots as roots_model,
    toe_inputs as toe_inputs_model,
    toe_ports as toe_ports_model,
    vulnerabilities as vulnerabilities_model,
)
from db_model.events.types import (
    EventMetadataToUpdate,
    GroupEventsRequest,
)
from db_model.roots.types import (
    IPRoot,
)
from db_model.toe_inputs.types import (
    RootToeInputsRequest,
    ToeInput,
)
from db_model.toe_ports.types import (
    RootToePortsRequest,
    ToePort,
)
from db_model.vulnerabilities.types import (
    VulnerabilityMetadataToUpdate,
)
import itertools
import logging
import logging.config
from newutils import (
    datetime as datetime_utils,
)
from organizations.domain import (
    get_all_active_group_names,
)
from settings import (
    LOGGING,
)
import time

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


def get_oldest_root(ip_roots: list[IPRoot]) -> IPRoot:
    return min(
        ip_roots,
        key=lambda ip_root: ip_root.created_date,
    )


async def add_toe_input(toe_input: ToeInput) -> None:
    with contextlib.suppress(RepeatedToeInput):
        await toe_inputs_model.add(toe_input=toe_input)


async def add_toe_port(toe_port: ToePort) -> None:
    with contextlib.suppress(RepeatedToePort):
        await toe_ports_model.add(toe_port=toe_port)


async def merge_roots(
    loaders: Dataloaders, ip_root: IPRoot, root_to_keep: IPRoot
) -> None:
    toe_inputs = await loaders.root_toe_inputs.load_nodes(
        RootToeInputsRequest(group_name=ip_root.group_name, root_id=ip_root.id)
    )
    await collect(
        add_toe_input(
            toe_input=toe_input._replace(
                state=toe_input.state._replace(
                    unreliable_root_id=root_to_keep.id
                )
            )
        )
        for toe_input in toe_inputs
    )
    await collect(
        toe_inputs_model.remove(
            entry_point=toe_input.entry_point,
            component=toe_input.component,
            group_name=toe_input.group_name,
            root_id=toe_input.state.unreliable_root_id,
        )
        for toe_input in toe_inputs
    )

    toe_ports = await loaders.root_toe_ports.load_nodes(
        RootToePortsRequest(group_name=ip_root.group_name, root_id=ip_root.id)
    )
    await collect(
        add_toe_port(toe_port=toe_port._replace(root_id=root_to_keep.id))
        for toe_port in toe_ports
    )
    await collect(
        toe_ports_model.remove(
            port=toe_port.port,
            address=toe_port.address,
            group_name=toe_port.group_name,
            root_id=toe_port.root_id,
        )
        for toe_port in toe_ports
    )
    group_events = await loaders.group_events.load(
        GroupEventsRequest(group_name=ip_root.group_name)
    )
    root_events = tuple(
        event for event in group_events if event.root_id == ip_root.id
    )
    await collect(
        tuple(
            events_model.update_metadata(
                event_id=event.id,
                group_name=event.group_name,
                metadata=EventMetadataToUpdate(root_id=root_to_keep.id),
            )
            for event in root_events
        )
    )
    vulnerabilities = await loaders.root_vulnerabilities.load(ip_root.id)
    await collect(
        tuple(
            vulnerabilities_model.update_metadata(
                finding_id=vulnerability.finding_id,
                vulnerability_id=vulnerability.id,
                metadata=VulnerabilityMetadataToUpdate(
                    root_id=root_to_keep.id
                ),
            )
            for vulnerability in vulnerabilities
        )
    )


async def process_address_roots(
    loaders: Dataloaders,
    address_info: dict[str, str | list[str]],
    ip_roots: list[IPRoot],
) -> None:
    ip_roots_by_nickname = {
        ip_root.state.nickname: ip_root for ip_root in ip_roots
    }
    root_to_keep = (
        ip_roots_by_nickname[str(address_info["new_nickname"])]
        if address_info["new_nickname"] in ip_roots_by_nickname
        else get_oldest_root(ip_roots)
    )
    for ip_root in ip_roots:
        if ip_root.id != root_to_keep.id:
            await merge_roots(loaders, ip_root, root_to_keep)
            await roots_model.remove(root_id=ip_root.id)

    if root_to_keep.state.nickname != address_info["new_nickname"]:
        await roots_model.update_root_state(
            group_name=root_to_keep.group_name,
            root_id=root_to_keep.id,
            current_value=root_to_keep.state,
            state=root_to_keep.state._replace(
                nickname=str(address_info["new_nickname"]),
                modified_date=datetime_utils.get_utc_now(),
                modified_by="integrates@fluidattacks.com",
            ),
        )


async def process_group(
    group_name: str,
    duplicated_ip_roots: dict[tuple[str, str], dict[str, str | list[str]]],
) -> None:
    loaders = get_new_context()
    group_roots = await loaders.group_roots.load(group_name)
    group_ip_roots = sorted(
        list(root for root in group_roots if isinstance(root, IPRoot)),
        key=lambda x: x.state.address,
    )
    for address, ip_roots in itertools.groupby(
        group_ip_roots, lambda x: x.state.address.strip()
    ):
        list_ip_roots = list(ip_roots)
        if len(list_ip_roots) > 1:
            await process_address_roots(
                loaders,
                duplicated_ip_roots[(group_name, address)],
                list_ip_roots,
            )

    LOGGER_CONSOLE.info(
        "Group processed",
        extra={
            "extra": {
                "group_name": group_name,
            }
        },
    )


async def main() -> None:
    loaders = get_new_context()
    with open(
        "duplicated_ip_roots.csv",
        mode="r",
        encoding="utf8",
    ) as in_file:
        reader = csv.reader(in_file)
        duplicated_ip_roots: dict[
            tuple[str, str], dict[str, str | list[str]]
        ] = {
            (str(row[0]).strip(), str(row[1]).strip()): dict(
                group_name=str(row[0]).strip(),
                address=str(row[1]).strip(),
                new_nickname=str(row[2]).strip(),
                current_nicknames=[
                    str(current_nickname).strip()
                    for current_nickname in row[3:]
                    if current_nickname
                ],
            )
            for row in reader
        }

    all_group_names = sorted(await get_all_active_group_names(loaders))
    count = 0
    LOGGER_CONSOLE.info(
        "All group names",
        extra={
            "extra": {
                "total": len(all_group_names),
            }
        },
    )
    for group_name in all_group_names:
        count += 1
        LOGGER_CONSOLE.info(
            "Group",
            extra={
                "extra": {
                    "group_name": group_name,
                    "count": count,
                }
            },
        )
        await process_group(group_name, duplicated_ip_roots)


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC"
    )
    print(f"{execution_time}\n{finalization_time}")
