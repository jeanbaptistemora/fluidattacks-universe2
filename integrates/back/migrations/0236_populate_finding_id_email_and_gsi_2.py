# type: ignore

# pylint: disable=invalid-name,import-error
"""
Populate the email in gsi_2 in finding_metadata

Execution Time:    2022-06-30 at 23:49:53 UTC
Finalization Time: 2022-06-30 at 23:51:59 UTC
"""

from aioextensions import (
    collect,
    run,
)
from authz.enforcer import (
    get_group_level_enforcer_legacy,
)
from boto3.dynamodb.conditions import (
    Attr,
    Key,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model import (
    TABLE,
)
from db_model.findings.constants import (
    ME_DRAFTS_INDEX_METADATA,
)
from db_model.findings.types import (
    Finding,
)
from db_model.findings.utils import (
    format_optional_state,
)
from db_model.groups.types import (
    Group,
)
from dynamodb import (
    keys,
    operations,
)
from dynamodb.historics import (
    get_metadata,
    get_optional_latest,
)
import logging
import logging.config
from organizations.domain import (
    get_all_active_groups,
)
from settings import (
    LOGGING,
)
import time

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")
PROD = True


async def populate_index(
    *, metadata: dict, draft_id: str, group_name: str
) -> None:
    key_structure = TABLE.primary_key
    gsi_2_index = TABLE.indexes["gsi_2"]
    user_email: str = metadata.get("analyst_email", "")
    if user_email:
        enforcer = await get_group_level_enforcer_legacy(
            user_email, with_cache=False
        )
        if not enforcer(group_name, "api_mutations_submit_draft_mutate"):
            user_email = ""

    gsi_2_key = keys.build_key(
        facet=ME_DRAFTS_INDEX_METADATA,
        values={
            "email": user_email,
            "id": draft_id,
        },
    )
    finding_item = {
        gsi_2_index.primary_key.partition_key: gsi_2_key.partition_key,
        gsi_2_index.primary_key.sort_key: gsi_2_key.sort_key,
    }

    metadata_key = keys.build_key(
        facet=TABLE.facets["finding_metadata"],
        values={"group_name": group_name, "id": draft_id},
    )
    if metadata.get(gsi_2_index.primary_key.partition_key) != finding_item.get(
        gsi_2_index.primary_key.partition_key
    ) or metadata.get(gsi_2_index.primary_key.sort_key) != finding_item.get(
        gsi_2_index.primary_key.sort_key
    ):
        LOGGER_CONSOLE.info(
            "Item is going to be updated!",
            extra={
                "extra": {
                    "finding_item": finding_item,
                    "gsi_2_index": gsi_2_index,
                    "finding_key": metadata_key,
                }
            },
        )
        if PROD:
            await operations.update_item(
                condition_expression=Attr(
                    key_structure.partition_key
                ).exists(),
                item=finding_item,
                key=metadata_key,
                table=TABLE,
            )
    else:
        LOGGER_CONSOLE.info(
            "Item is not going to be updated!",
            extra={
                "extra": {
                    "finding_key": metadata_key,
                }
            },
        )


async def populate_by_draft(
    *,
    draft: Finding,
    group_name: str,
) -> None:
    primary_key = keys.build_key(
        facet=TABLE.facets["finding_metadata"],
        values={"group_name": group_name, "id": draft.id},
    )

    index = TABLE.indexes["inverted_index"]
    key_structure = index.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.sort_key)
            & Key(key_structure.sort_key).begins_with(
                primary_key.partition_key
            )
        ),
        facets=(
            TABLE.facets["finding_approval"],
            TABLE.facets["finding_creation"],
            TABLE.facets["finding_metadata"],
            TABLE.facets["finding_state"],
            TABLE.facets["finding_submission"],
            TABLE.facets["finding_unreliable_indicators"],
            TABLE.facets["finding_verification"],
        ),
        index=index,
        table=TABLE,
    )

    if not response.items:
        return

    metadata = get_metadata(
        item_id=primary_key.partition_key,
        key_structure=key_structure,
        raw_items=response.items,
    )

    approval = format_optional_state(
        get_optional_latest(
            item_id=primary_key.partition_key,
            key_structure=key_structure,
            historic_suffix="APPROVAL",
            raw_items=response.items,
        )
    )
    if approval is not None:
        return

    await populate_index(
        metadata=metadata, draft_id=draft.id, group_name=group_name
    )


async def process_group(
    *,
    group: Group,
    loaders: Dataloaders,
    progress: float,
) -> None:
    LOGGER_CONSOLE.info(
        "Working on group",
        extra={
            "extra": {
                "group_name": group.name,
                "progress": round(progress, 2),
            }
        },
    )
    group_drafts = await loaders.group_drafts.load(group.name)
    await collect(
        tuple(
            populate_by_draft(draft=draft, group_name=group.name)
            for draft in group_drafts
        ),
        workers=16,
    )


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    active_groups = await get_all_active_groups(loaders)
    LOGGER_CONSOLE.info(
        "Active groups",
        extra={"extra": {"groups_len": len(active_groups)}},
    )

    await collect(
        tuple(
            process_group(
                group=group,
                loaders=loaders,
                progress=count / len(active_groups),
            )
            for count, group in enumerate(active_groups)
        ),
        workers=4,
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
