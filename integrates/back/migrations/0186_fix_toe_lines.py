# pylint: disable=invalid-name
"""
Fix the attacked lines since the last migration from the services repo does not
take into account the loc.
"""

from aioextensions import (
    collect,
    run,
)
from custom_exceptions import (
    ToeLinesAlreadyUpdated,
)
from dataloaders import (
    get_new_context,
)
from db_model import (
    toe_lines as toe_lines_model,
)
from db_model.toe_lines.types import (
    GroupToeLinesRequest,
    ToeLines,
    ToeLinesConnection,
    ToeLinesMetadataToUpdate,
)
from decorators import (
    retry_on_exceptions,
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
from typing import (
    Tuple,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER_CONSOLE = logging.getLogger("console")


@retry_on_exceptions(
    exceptions=(UnavailabilityError, ToeLinesAlreadyUpdated),
)
async def process_group_lines(
    current_toe_lines: ToeLines,
) -> None:
    if current_toe_lines.attacked_lines > current_toe_lines.loc:
        new_attacked_lines = current_toe_lines.loc
        metadata = ToeLinesMetadataToUpdate(
            attacked_lines=new_attacked_lines,
        )
        await toe_lines_model.update_metadata(
            current_value=current_toe_lines,
            metadata=metadata,
        )


async def main() -> None:
    loaders = get_new_context()
    group_names = tuple(
        group["project_name"]
        for group in await groups_domain.get_all(attributes=["project_name"])
    )
    LOGGER_CONSOLE.info("Getting lines", extra={"extra": {}})
    groups_toe_lines_connections: Tuple[
        ToeLinesConnection, ...
    ] = await loaders.group_toe_lines.load_many(
        [
            GroupToeLinesRequest(group_name=group_name)
            for group_name in group_names
        ]
    )
    groups_len = len(group_names)
    for (index, group_toe_lines_connection, group_name,) in zip(
        range(groups_len),
        groups_toe_lines_connections,
        group_names,
    ):
        await collect(
            tuple(
                process_group_lines(toe_lines)
                for toe_lines in [
                    edge.node for edge in group_toe_lines_connection.edges
                ]
            ),
            workers=1000,
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
