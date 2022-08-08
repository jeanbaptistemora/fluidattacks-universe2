# pylint: disable=invalid-name
"""
update managed field type from boolean to enum
"""

from aioextensions import (
    collect,
    run,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.groups.types import (
    Group,
    GroupState,
)
from enum import (
    Enum,
)
from groups import (
    domain as groups_domain,
)
import logging
import logging.config
from newutils import (
    datetime as datetime_utils,
)
from organizations.domain import (
    iterate_organizations_and_groups,
)
from settings import (
    LOGGING,
)
import time

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


class GroupManaged(str, Enum):
    MANAGED: str = "MANAGED"
    NOT_MANAGED: str = "NOT_MANAGED"
    UNDER_REVIEW: str = "UNDER_REVIEW"
    TRIAL: str = "TRIAL"


async def process_group(
    loaders: Dataloaders,
    group_name: str,
    progress: float,
) -> None:
    group: Group = await loaders.group.load(group_name)

    await groups_domain.update_state(
        group_name=group_name,
        organization_id=group.organization_id,
        state=GroupState(
            comments=group.state.comments,
            modified_date=datetime_utils.get_iso_date(),
            has_machine=group.state.has_machine,
            has_squad=group.state.has_squad,
            managed=GroupManaged("NOT_MANAGED"),
            justification=group.state.justification,
            modified_by=group.state.modified_by,
            payment_id=group.state.payment_id,
            service=group.state.service,
            status=group.state.status,
            tier=group.state.tier,
            type=group.state.type,
        ),
    )

    LOGGER_CONSOLE.info(
        "Group processed",
        extra={
            "extra": {
                "group_name": group_name,
                "progress": round(progress, 2),
            }
        },
    )


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    group_names = []
    async for _, _, org_group_names in iterate_organizations_and_groups(
        loaders
    ):
        group_names.extend(org_group_names)
    group_names_len = len(group_names)
    LOGGER_CONSOLE.info(
        "All groups",
        extra={
            "extra": {
                "group_names_len": group_names_len,
            }
        },
    )
    await collect(
        tuple(
            process_group(
                loaders=loaders,
                group_name=group_name,
                progress=count / group_names_len,
            )
            for count, group_name in enumerate(set(group_names))
        ),
        workers=2,
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
