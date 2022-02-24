# pylint: disable=invalid-name
"""
Remove services toe lines from asm.
"""

from aioextensions import (
    collect,
    run,
)
from dataloaders import (
    get_new_context,
)
from db_model import (
    services_toe_lines as services_toe_lines_model,
)
from db_model.services_toe_lines.types import (
    ServicesToeLines,
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
    exceptions=(UnavailabilityError,),
)
async def process_services_lines(
    services_lines: ServicesToeLines,
) -> None:
    await services_toe_lines_model.remove(
        filename=services_lines.filename,
        group_name=services_lines.group_name,
        root_id=services_lines.root_id,
    )


async def main() -> None:
    loaders = get_new_context()
    group_names = tuple(
        group["project_name"]
        for group in await groups_domain.get_all(attributes=["project_name"])
    )
    groups_len = len(group_names)
    for (index, group_name) in zip(range(groups_len), group_names):
        group_services_toe_lines: Tuple[
            ServicesToeLines, ...
        ] = await loaders.group_services_toe_lines.load(group_name)
        await collect(
            tuple(
                process_services_lines(services_toe_lines)
                for services_toe_lines in group_services_toe_lines
            ),
            workers=5000,
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
