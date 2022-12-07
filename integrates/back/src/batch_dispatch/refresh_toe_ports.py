from aioextensions import (
    collect,
)
from batch.dal import (
    delete_action,
)
from batch.types import (
    BatchProcessing,
)
from custom_exceptions import (
    RepeatedToePort,
    ToePortAlreadyUpdated,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model.roots.enums import (
    RootStatus,
)
from db_model.roots.types import (
    IPRoot,
    Root,
)
from db_model.toe_ports.types import (
    RootToePortsRequest,
    ToePort,
)
from decorators import (
    retry_on_exceptions,
)
from dynamodb.exceptions import (
    UnavailabilityError,
)
import logging
import logging.config
from settings import (
    LOGGING,
)
from toe.ports import (
    domain as toe_ports_domain,
)
from toe.ports.types import (
    ToePortAttributesToUpdate,
)
from typing import (
    Optional,
    Tuple,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


toe_ports_update = retry_on_exceptions(
    exceptions=(UnavailabilityError,), sleep_seconds=5
)(toe_ports_domain.update)


def get_non_present_toe_ports_to_update(
    root: IPRoot,
    root_toe_ports: tuple[ToePort, ...],
) -> Tuple[Tuple[ToePort, ToePortAttributesToUpdate], ...]:
    LOGGER.info(
        "Getting non present toe ports to update",
        extra={
            "extra": {
                "repo_nickname": root.state.nickname,
            }
        },
    )
    return tuple(
        (
            toe_port,
            ToePortAttributesToUpdate(be_present=False),
        )
        for toe_port in root_toe_ports
        if root.state.status == RootStatus.INACTIVE and toe_port.be_present
    )


async def refresh_inactive_root_toe_ports(
    loaders: Dataloaders,
    group_name: str,
    root: IPRoot,
) -> None:
    LOGGER.info(
        "Refreshing inactive toe ports",
        extra={
            "extra": {
                "repo_nickname": root.state.nickname,
            }
        },
    )
    root_toe_ports = await loaders.root_toe_ports.load_nodes(
        RootToePortsRequest(group_name=group_name, root_id=root.id)
    )
    non_present_toe_ports_to_update = get_non_present_toe_ports_to_update(
        root, root_toe_ports
    )
    await collect(
        tuple(
            toe_ports_update(
                current_value, attrs_to_update, is_moving_toe_port=True
            )
            for current_value, attrs_to_update in (
                non_present_toe_ports_to_update
            )
        ),
    )
    LOGGER.info(
        "Finish refreshing inactive toe ports",
        extra={
            "extra": {
                "repo_nickname": root.state.nickname,
            }
        },
    )


@retry_on_exceptions(
    exceptions=(
        RepeatedToePort,
        ToePortAlreadyUpdated,
    ),
)
async def refresh_root_toe_ports(
    group_name: str, optional_repo_nickname: Optional[str]
) -> None:
    loaders = get_new_context()
    roots: Tuple[Root, ...] = await loaders.group_roots.load(group_name)
    # There are roots with the same nickname
    # then it is going to take the last modified root
    sorted_roots = sorted(
        roots,
        key=lambda root: datetime.fromisoformat(root.state.modified_date),
    )
    active_roots = {
        root.state.nickname: root
        for root in sorted_roots
        if isinstance(root, IPRoot) and root.state.status == RootStatus.ACTIVE
    }
    # Deactivate all the toe ports for all the inactive roots
    # with the same nickname
    inactive_roots = tuple(
        root
        for root in sorted_roots
        if isinstance(root, IPRoot)
        and root.state.status == RootStatus.INACTIVE
        and root.state.nickname not in active_roots
    )
    inactive_roots_to_proccess = tuple(
        root_repo
        for root_repo in inactive_roots
        if not optional_repo_nickname
        or root_repo.state.nickname == optional_repo_nickname
    )
    for root in inactive_roots_to_proccess:
        await refresh_inactive_root_toe_ports(loaders, group_name, root)


async def refresh_toe_ports(*, item: BatchProcessing) -> None:
    group_name: str = item.entity
    optional_repo_nickname: Optional[str] = (
        None if item.additional_info == "*" else item.additional_info
    )
    await refresh_root_toe_ports(group_name, optional_repo_nickname)
    await delete_action(
        action_name=item.action_name,
        additional_info=item.additional_info,
        entity=item.entity,
        subject=item.subject,
        time=item.time,
    )
