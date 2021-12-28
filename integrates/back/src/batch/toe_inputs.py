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
    RepeatedToeInput,
    ToeInputAlreadyUpdated,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model.roots.types import (
    GitRootItem,
    RootItem,
    URLRootItem,
)
from db_model.toe_inputs.types import (
    GroupToeInputsRequest,
    ToeInput,
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
from toe.inputs import (
    domain as toe_inputs_domain,
)
from toe.inputs.types import (
    ToeInputAttributesToUpdate,
)
from typing import (
    Dict,
    Optional,
    Tuple,
    Union,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")

toe_inputs_update = retry_on_exceptions(
    exceptions=(UnavailabilityError,), sleep_seconds=5
)(toe_inputs_domain.update)


def get_non_present_toe_inputs_to_update(
    root: Union[GitRootItem, URLRootItem],
    root_toe_inputs: Dict[str, ToeInput],
) -> Tuple[Tuple[ToeInput, ToeInputAttributesToUpdate], ...]:
    LOGGER_CONSOLE.info(
        "Getting non present toe inputs to update",
        extra={
            "extra": {
                "repo_nickname": root.state.nickname,
            }
        },
    )
    return tuple(
        (
            root_toe_inputs[toe_input_hash],
            ToeInputAttributesToUpdate(
                be_present=False,
            ),
        )
        for toe_input_hash in root_toe_inputs
        if root.state.status == "INACTIVE"
    )


async def refresh_inactive_root_toe_inputs(
    loaders: Dataloaders,
    group_name: str,
    root: Union[GitRootItem, URLRootItem],
) -> None:
    LOGGER_CONSOLE.info(
        "Refreshing inactive toe inputs",
        extra={
            "extra": {
                "repo_nickname": root.state.nickname,
            }
        },
    )
    root_toe_inputs = {
        toe_input.get_hash(): toe_input
        for toe_input in await loaders.group_toe_inputs.load_nodes(
            GroupToeInputsRequest(group_name=group_name)
        )
    }
    non_present_toe_inputs_to_update = get_non_present_toe_inputs_to_update(
        root, root_toe_inputs
    )
    await collect(
        tuple(
            toe_inputs_update(current_value, attrs_to_update)
            for current_value, attrs_to_update in (
                non_present_toe_inputs_to_update
            )
        ),
    )
    LOGGER_CONSOLE.info(
        "Finish refreshing inactive toe inputs",
        extra={
            "extra": {
                "repo_nickname": root.state.nickname,
            }
        },
    )


@retry_on_exceptions(
    exceptions=(
        RepeatedToeInput,
        ToeInputAlreadyUpdated,
    ),
)
async def refresh_root_toe_inputs(
    group_name: str, optional_repo_nickname: Optional[str]
) -> None:
    loaders = get_new_context()
    roots: Tuple[RootItem, ...] = await loaders.group_roots.load(group_name)
    # There are roots with the same nickname
    # then it is going to take the last modified root
    sorted_roots = sorted(
        roots,
        key=lambda root: datetime.fromisoformat(root.state.modified_date),
    )
    active_roots = {
        root.state.nickname: root
        for root in sorted_roots
        if isinstance(root, (GitRootItem, URLRootItem))
        and root.state.status == "ACTIVE"
    }
    # Deactivate all the toe inputs for all the inactive roots
    # with the same nickname
    inactive_roots = tuple(
        root
        for root in sorted_roots
        if isinstance(root, (GitRootItem, URLRootItem))
        and root.state.status == "INACTIVE"
        and root.state.nickname not in active_roots
    )
    inactive_root_to_proccess = tuple(
        root_repo
        for root_repo in inactive_roots
        if not optional_repo_nickname
        or root_repo.state.nickname == optional_repo_nickname
    )
    for root in inactive_root_to_proccess:
        await refresh_inactive_root_toe_inputs(loaders, group_name, root)


async def refresh_toe_inputs(*, item: BatchProcessing) -> None:
    group_name: str = item.entity
    optional_repo_nickname: Optional[str] = (
        None if item.additional_info == "*" else item.additional_info
    )
    await refresh_root_toe_inputs(group_name, optional_repo_nickname)
    await delete_action(
        action_name=item.action_name,
        additional_info=item.additional_info,
        entity=item.entity,
        subject=item.subject,
        time=item.time,
    )
