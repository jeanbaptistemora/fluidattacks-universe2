# pylint: disable=invalid-name
"""
Fix attacked lines and state modified date in toe lines
"""
from aioextensions import (
    collect,
    run,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model import (
    toe_lines as toe_lines_model,
)
from db_model.toe_lines.types import (
    GroupToeLinesRequest,
    ToeLinesMetadataToUpdate,
)
import logging
import logging.config
from newutils import (
    datetime as datetime_utils,
)
from organizations import (
    domain as orgs_domain,
)
from settings import (
    LOGGING,
)
import time

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


async def process_group(group_name: str) -> None:
    group_toe_lines = await get_new_context().group_toe_lines.load_nodes(
        GroupToeLinesRequest(group_name=group_name)
    )
    await collect(
        tuple(
            toe_lines_model.update_metadata(
                current_value=toe_lines,
                metadata=ToeLinesMetadataToUpdate(
                    attacked_lines=toe_lines.loc,
                    state=toe_lines.state._replace(
                        modified_date=datetime_utils.get_utc_now()
                    ),
                ),
            )
            for toe_lines in group_toe_lines
            if (
                toe_lines.attacked_at is not None
                and toe_lines.attacked_at > toe_lines.modified_date
                and toe_lines.attacked_lines == 0
            )
        )
    )
    LOGGER_CONSOLE.info(
        "Group processed attacked_lines",
        extra={
            "extra": {
                "group_name": group_name,
            }
        },
    )

    group_toe_lines = await get_new_context().group_toe_lines.load_nodes(
        GroupToeLinesRequest(group_name=group_name)
    )
    await collect(
        tuple(
            toe_lines_model.update_metadata(
                current_value=toe_lines,
                metadata=ToeLinesMetadataToUpdate(
                    state=toe_lines.state._replace(
                        modified_date=datetime_utils.get_utc_now()
                    ),
                ),
            )
            for toe_lines in group_toe_lines
            if toe_lines.state.modified_date == toe_lines.modified_date
        )
    )

    LOGGER_CONSOLE.info(
        "Group processed state modified_date",
        extra={
            "extra": {
                "group_name": group_name,
            }
        },
    )


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    all_group_names = sorted(
        await orgs_domain.get_all_active_group_names(loaders)
    )
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
        await process_group(group_name)


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S %Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S %Z"
    )
    print(f"{execution_time}\n{finalization_time}")
