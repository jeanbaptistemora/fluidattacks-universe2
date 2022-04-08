# pylint: disable=invalid-name
"""
Add the root id into the sort keys for toe inputs

Execution Time:    2022-02-22 at 02:31:28 UTC
Finalization Time: 2022-02-22 at 03:40:15 UTC
"""

from aioextensions import (
    collect,
    run,
)
from contextlib import (
    suppress,
)
from custom_exceptions import (
    RepeatedToeInput,
)
from dataloaders import (
    get_new_context,
)
from db_model import (
    TABLE,
    toe_inputs as toe_inputs_model,
)
from db_model.toe_inputs.constants import (
    OLD_INPUT_FACET,
)
from db_model.toe_inputs.types import (
    GroupToeInputsRequest,
    ToeInput,
    ToeInputsConnection,
)
from decorators import (
    retry_on_exceptions,
)
from dynamodb import (
    keys,
    operations,
)
from dynamodb.exceptions import (
    UnavailabilityError,
)
from groups import (
    domain as groups_domain,
)
import logging
import logging.config
from settings import (
    LOGGING,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER_CONSOLE = logging.getLogger("console")


@retry_on_exceptions(
    exceptions=(UnavailabilityError,),
)
async def add_input(
    current_toe_input: ToeInput,
) -> None:
    new_toe_input = ToeInput(
        attacked_at=current_toe_input.attacked_at,
        attacked_by=current_toe_input.attacked_by,
        be_present=current_toe_input.be_present,
        be_present_until=current_toe_input.be_present_until,
        component=current_toe_input.component,
        entry_point=current_toe_input.entry_point,
        first_attack_at=current_toe_input.first_attack_at,
        group_name=current_toe_input.group_name,
        has_vulnerabilities=current_toe_input.has_vulnerabilities,
        seen_at=current_toe_input.seen_at,
        seen_first_time_by=current_toe_input.seen_first_time_by,
        unreliable_root_id=current_toe_input.unreliable_root_id,
    )
    await toe_inputs_model.add(toe_input=new_toe_input)


@retry_on_exceptions(
    exceptions=(UnavailabilityError,),
)
async def remove_input(
    current_toe_input: ToeInput,
) -> None:
    toe_input_key = keys.build_key(
        facet=OLD_INPUT_FACET,
        values={
            "component": current_toe_input.component,
            "entry_point": current_toe_input.entry_point,
            "group_name": current_toe_input.group_name,
        },
    )
    await operations.delete_item(key=toe_input_key, table=TABLE)


async def process_input(
    current_toe_input: ToeInput,
) -> None:
    with suppress(RepeatedToeInput):
        await add_input(current_toe_input)
    await remove_input(current_toe_input)


async def main() -> None:
    loaders = get_new_context()
    group_names = tuple(
        group["project_name"]
        for group in await groups_domain.get_all(attributes=["project_name"])
    )
    LOGGER_CONSOLE.info("Getting inputs")
    groups_len = len(group_names)
    for (index, group_name) in zip(range(groups_len), group_names):
        group_toe_input_connection: ToeInputsConnection = (
            await loaders.group_toe_inputs.load(
                GroupToeInputsRequest(group_name=group_name)
            )
        )
        await collect(
            tuple(
                process_input(toe_input)
                for toe_input in [
                    edge.node for edge in group_toe_input_connection.edges
                ]
            )
        )
        LOGGER_CONSOLE.info(
            "Group updated",
            extra={
                "extra": {
                    "group_name": group_name,
                    "progress": str(index / groups_len),
                }
            },
        )


if __name__ == "__main__":
    run(main())
