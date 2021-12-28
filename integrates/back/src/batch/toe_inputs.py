from db_model.roots.types import (
    GitRootItem,
    URLRootItem,
)
from db_model.toe_inputs.types import (
    ToeInput,
)
import logging
import logging.config
from settings import (
    LOGGING,
)
from toe.inputs.types import (
    ToeInputAttributesToUpdate,
)
from toe.lines.types import (
    ToeLinesAttributesToUpdate,
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


def get_non_present_toe_inputs_to_update(
    root: Union[GitRootItem, URLRootItem],
    root_toe_inputs: Dict[str, ToeInput],
) -> Tuple[Tuple[ToeInput, ToeLinesAttributesToUpdate], ...]:
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
