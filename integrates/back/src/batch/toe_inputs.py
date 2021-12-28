from aioextensions import (
    collect,
)
from dataloaders import (
    Dataloaders,
)
from db_model.roots.types import (
    GitRootItem,
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
