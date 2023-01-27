# type: ignore

# pylint: disable=invalid-name
"""
update managed field type from boolean to enum

Execution Time:    2022-08-10 at 12:44:32 UTC
Finalization Time: 2022-08-10 at 12:46:11 UTC
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
    TABLE,
)
from db_model.groups.types import (
    Group,
    GroupState,
)
from dynamodb import (
    keys,
    operations,
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
import simplejson as json
import time

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


class GroupManaged(str, Enum):
    MANAGED: str = "MANAGED"
    NOT_MANAGED: str = "NOT_MANAGED"
    UNDER_REVIEW: str = "UNDER_REVIEW"
    TRIAL: str = "TRIAL"


async def process_historic_state(
    group_name: str,
    state: GroupState,
) -> None:
    key_structure = TABLE.primary_key
    state_item = json.loads(json.dumps(state))
    state_item = {
        key: None if not value and value is not False else value
        for key, value in state_item.items()
        if value is not None
    }
    historic_state_key = keys.build_key(
        facet=TABLE.facets["group_historic_state"],
        values={
            "name": group_name,
            "iso8601utc": state.modified_date,
        },
    )
    historic_item = {
        key_structure.partition_key: historic_state_key.partition_key,
        key_structure.sort_key: historic_state_key.sort_key,
        **state_item,
    }
    await operations.put_item(
        facet=TABLE.facets["group_historic_state"],
        item=historic_item,
        table=TABLE,
    )


async def process_group(
    loaders: Dataloaders,
    group_name: str,
    progress: float,
) -> None:
    historic: list[GroupState] = await loaders.group_historic_state.load(
        group_name
    )

    await collect(
        tuple(
            process_historic_state(
                group_name=group_name,
                state=GroupState(
                    comments=state.comments,
                    modified_date=state.modified_date,
                    has_machine=state.has_machine,
                    has_squad=state.has_squad,
                    managed=GroupManaged("MANAGED")
                    if state.managed is True
                    else GroupManaged("NOT_MANAGED"),
                    justification=state.justification,
                    modified_by=state.modified_by,
                    payment_id=state.payment_id,
                    pending_deletion_date=state.pending_deletion_date,
                    service=state.service,
                    status=state.status,
                    tier=state.tier,
                    type=state.type,
                ),
            )
            for state in historic
        ),
        workers=2,
    )

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
            pending_deletion_date=group.state.pending_deletion_date,
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
