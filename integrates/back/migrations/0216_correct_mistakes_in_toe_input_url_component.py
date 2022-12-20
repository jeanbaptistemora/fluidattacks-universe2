# pylint: disable=invalid-name
"""
Correct mistakes for url roots in the toe inputs that belong to Kasur.

Execution Time:    2022-05-16 at 22:02:39 UTC
Finalization Time: 2022-05-16 at 22:03:07 UTC
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
    toe_inputs as toe_inputs_model,
)
from db_model.roots.types import (
    Root,
    URLRoot,
)
from db_model.toe_inputs.types import (
    GroupToeInputsRequest,
    ToeInput,
    ToeInputsConnection,
    ToeInputState,
)
from decorators import (
    retry_on_exceptions,
)
from dynamodb.exceptions import (
    UnavailabilityError,
)
import logging
import logging.config
from newutils.datetime import (
    get_utc_now,
)
from settings import (
    LOGGING,
)
import time

logging.config.dictConfig(LOGGING)

# Constants
LOGGER_CONSOLE = logging.getLogger("console")


@retry_on_exceptions(
    exceptions=(UnavailabilityError,),
)
async def add_input(current_toe_input: ToeInput, new_component: str) -> None:
    new_toe_input = ToeInput(
        component=new_component,
        entry_point=current_toe_input.entry_point,
        group_name=current_toe_input.group_name,
        state=ToeInputState(
            attacked_at=current_toe_input.state.attacked_at,
            attacked_by=current_toe_input.state.attacked_by,
            be_present=current_toe_input.state.be_present,
            be_present_until=current_toe_input.state.be_present_until,
            first_attack_at=current_toe_input.state.first_attack_at,
            has_vulnerabilities=current_toe_input.state.has_vulnerabilities,
            modified_by="machine@fluidattacks.com",
            modified_date=get_utc_now(),
            seen_at=current_toe_input.state.seen_at,
            seen_first_time_by=current_toe_input.state.seen_first_time_by,
            unreliable_root_id=current_toe_input.state.unreliable_root_id,
        ),
    )
    await toe_inputs_model.add(toe_input=new_toe_input)


@retry_on_exceptions(
    exceptions=(UnavailabilityError,),
)
async def remove_input(
    current_toe_input: ToeInput,
) -> None:
    await toe_inputs_model.remove(
        entry_point=current_toe_input.entry_point,
        component=current_toe_input.component,
        group_name=current_toe_input.group_name,
        root_id=current_toe_input.state.unreliable_root_id,
    )


async def process_input(
    current_toe_input: ToeInput, roots: tuple[Root, ...]
) -> None:
    root_id = current_toe_input.state.unreliable_root_id
    root = next(
        (root for root in roots if root.id == root_id),
        None,
    )
    if isinstance(root, URLRoot):
        url_root_host = (
            f"{root.state.protocol.lower()}://{root.state.host}:"
            f"{root.state.port}{root.state.path}"
            if root.state.port
            else (
                f"{root.state.protocol.lower()}://{root.state.host}"
                f"{root.state.path}"
            )
        ).removesuffix("/")
        if url_root_host != current_toe_input.component and (
            url_root_host in current_toe_input.component
        ):
            if (
                formatted_new_host := f"{url_root_host}/"
            ) not in current_toe_input.component:
                new_component = current_toe_input.component.replace(
                    url_root_host, formatted_new_host
                )
                with suppress(RepeatedToeInput):
                    await add_input(current_toe_input, new_component)
                await remove_input(current_toe_input)


async def main() -> None:
    loaders = get_new_context()
    group_names = ["kasur"]
    LOGGER_CONSOLE.info("Getting inputs")
    groups_len = len(group_names)
    for (index, group_name) in zip(range(groups_len), group_names):
        group_toe_input_connection: ToeInputsConnection = (
            await loaders.group_toe_inputs.load(
                GroupToeInputsRequest(group_name=group_name)
            )
        )
        roots: tuple[Root, ...] = await loaders.group_roots.load(group_name)
        await collect(
            tuple(
                process_input(toe_input, roots)
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
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC"
    )
    print(f"{execution_time}\n{finalization_time}")
