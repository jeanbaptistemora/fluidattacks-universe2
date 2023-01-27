# pylint: disable=invalid-name
# type: ignore
"""
update tags field to historic state

First Execution Time:     2022-10-27 at 04:53:24 UTC
First Finalization Time:  2022-10-27 at 04:57:50 UTC
Second Execution Time:    2022-10-27 at 05:00:12 UTC
Second Finalization Time: 2022-10-27 at 05:05:46 UTC
Remove Tags Execution Time:    2022-11-02 at 04:05:29 UTC
Remove Tags Finalization Time: 2022-11-02 at 04:06:55 UTC
"""

from aioextensions import (
    collect,
    run,
)
from boto3.dynamodb.conditions import (
    Attr,
    Key,
)
from custom_exceptions import (
    GroupNotFound,
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
from db_model.groups.utils import (
    serialize_sets,
)
from db_model.organizations.utils import (
    remove_org_id_prefix,
)
from dynamodb import (
    keys,
    operations,
)
from dynamodb.exceptions import (
    ConditionalCheckFailedException,
)
from itertools import (
    chain,
)
import logging
import logging.config
from organizations.domain import (
    get_group_names,
    iterate_organizations,
)
from settings import (
    LOGGING,
)
import simplejson as json
import time

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


async def _get_group(*, group_name: str) -> dict:
    primary_key = keys.build_key(
        facet=TABLE.facets["group_metadata"],
        values={"name": group_name},
    )

    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(TABLE.facets["group_metadata"],),
        limit=1,
        table=TABLE,
    )

    if not response.items:
        raise GroupNotFound()

    return response.items[0]


async def update_metadata(
    *,
    group_name: str,
    organization_id: str,
) -> None:
    key_structure = TABLE.primary_key

    try:
        primary_key = keys.build_key(
            facet=TABLE.facets["group_metadata"],
            values={
                "name": group_name,
                "organization_id": remove_org_id_prefix(organization_id),
            },
        )
        item = {"tags": None}
        condition_expression = Attr(key_structure.partition_key).exists()
        await operations.update_item(
            condition_expression=condition_expression,
            item=item,
            key=primary_key,
            table=TABLE,
        )
    except ConditionalCheckFailedException as ex:
        LOGGER_CONSOLE.info(
            "An error", extra={"extra": {"Exception": ex, "group": group_name}}
        )


async def process_historic_state(
    group_name: str,
    state: GroupState,
) -> None:
    key_structure = TABLE.primary_key
    state_item = json.loads(json.dumps(state, default=serialize_sets))
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


async def _process_group(
    *,
    group_name: str,
    progress: float,
) -> None:
    group: dict = await _get_group(group_name=group_name)

    if group.get("tags", None) or "tags" in group:
        LOGGER_CONSOLE.info(
            "Removing tags from group metadata",
            extra={
                "extra": {
                    "group_name": group_name,
                    "organization_id": group["organization_id"],
                    "tags": group["state"].get("tags"),
                }
            },
        )
        await update_metadata(
            group_name=group["name"], organization_id=group["organization_id"]
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


async def process_group(
    loaders: Dataloaders,
    group_name: str,
    progress: float,
) -> None:
    historic = await loaders.group_historic_state.load(group_name)
    group: Group = await loaders.group.load(group_name)
    if group.tags is None:
        return

    await collect(
        tuple(
            process_historic_state(
                group_name=group_name,
                state=GroupState(
                    comments=state.comments,
                    modified_date=state.modified_date,
                    has_machine=state.has_machine,
                    has_squad=state.has_squad,
                    managed=state.managed,
                    justification=state.justification,
                    modified_by=state.modified_by,
                    payment_id=state.payment_id,
                    pending_deletion_date=state.pending_deletion_date,
                    service=state.service,
                    status=state.status,
                    tags=group.tags,
                    tier=state.tier,
                    type=state.type,
                ),
            )
            for state in historic
            if state.tags != group.tags
        ),
        workers=2,
    )

    if group.tags != group.state.tags:
        await update_metadata(
            group_name=group_name,
            organization_id=group.organization_id,
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
    all_organization_ids = {"ORG#unknown"}
    async for organization in iterate_organizations():
        all_organization_ids.add(organization.id)

    all_group_names: list[str] = list(
        sorted(
            tuple(
                chain.from_iterable(
                    await collect(
                        tuple(
                            get_group_names(loaders, organization_id)
                            for organization_id in all_organization_ids
                        ),
                        workers=32,
                    )
                )
            )
        )
    )
    LOGGER_CONSOLE.info(
        "All groups",
        extra={"extra": {"groups_len": len(all_group_names)}},
    )
    await collect(
        tuple(
            _process_group(
                group_name=group_name,
                progress=count / len(set(all_group_names)),
            )
            for count, group_name in enumerate(set(all_group_names))
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
