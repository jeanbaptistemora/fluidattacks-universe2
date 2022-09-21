# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# pylint: disable=invalid-name
"""
Identify and fix findings with formatting inconsistencies, due to errors
in migrations 0238 and 0239.
These findings were left out as migrations only ran on active groups.

Execution Time:
Finalization Time:
"""

from aioextensions import (
    run,
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
from dynamodb import (
    keys,
    operations,
    operations_legacy as ops_legacy,
)
from dynamodb.types import (
    Item,
)
from organizations.domain import (
    get_all_deleted_groups,
)
import time
from typing import (
    Optional,
)


async def _has_inconsistencies_in_group(
    loaders: Dataloaders, group_name: str
) -> bool:
    try:
        await loaders.group_drafts_and_findings.load(group_name)
        return False
    except KeyError:
        return True


async def _get_findings_items(group_name: str) -> list[Item]:
    query_attrs = {
        "KeyConditionExpression": (
            Key("sk").eq(f"GROUP#{group_name}") & Key("pk").begins_with("FIN#")
        ),
        "IndexName": "inverted_index",
    }

    return await ops_legacy.query(TABLE.name, query_attrs)


def _get_milestone_item(
    finding_id: str, milestones_items: list[Item], suffix: str
) -> Optional[Item]:
    item = next(
        (
            item
            for item in milestones_items
            if item.get("pk") == f"FIN#{finding_id}#{suffix}"
        ),
        None,
    )
    if item:
        del item["pk"]
        del item["sk"]

    return item


async def _process_finding(
    finding_id: str, metadata: Item, milestones_items: list[Item]
) -> None:
    state = _get_milestone_item(finding_id, milestones_items, "STATE")
    creation = _get_milestone_item(finding_id, milestones_items, "CREATION")
    indicators = _get_milestone_item(
        finding_id, milestones_items, "UNRELIABLEINDICATORS"
    )
    approval = _get_milestone_item(finding_id, milestones_items, "APPROVAL")
    submission = _get_milestone_item(
        finding_id, milestones_items, "SUBMISSION"
    )
    verification = _get_milestone_item(
        finding_id, milestones_items, "VERIFICATION"
    )
    item = {
        "state": state,
        "creation": creation,
        "unreliable_indicators": indicators,
    }
    if approval:
        item["approval"] = approval
    if submission:
        item["submission"] = submission
    if verification:
        item["verification"] = verification

    key_structure = TABLE.primary_key
    primary_key = keys.build_key(
        facet=TABLE.facets["finding_metadata"],
        values={"group_name": metadata["group_name"], "id": finding_id},
    )
    await operations.update_item(
        condition_expression=Attr(key_structure.partition_key).exists(),
        item=item,
        key=primary_key,
        table=TABLE,
    )


async def _fix_formatting_at_group_findings(group_name: str) -> None:
    items = await _get_findings_items(group_name)
    metadata_items = [
        item for item in items if "id" in item and "group_name" in item
    ]
    for metadata in metadata_items:
        finding_id = metadata["id"]
        milestones_items = [
            item
            for item in items
            if str(item["pk"]).startswith(f"FIN#{finding_id}#")
        ]
        await _process_finding(finding_id, metadata, milestones_items)


async def _process_group(
    *,
    group_name: str,
    loaders: Dataloaders,
    progress: float,
) -> None:
    if await _has_inconsistencies_in_group(loaders, group_name):
        print(f"Formatting issue at {group_name=}")
        await _fix_formatting_at_group_findings(group_name)

    print(f"Group processed: {group_name=}, progress: {round(progress, 2)}")


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    group_names = sorted(
        [group.name for group in await get_all_deleted_groups(loaders)]
    )
    print(f"Groups to process: {len(group_names)=}")
    for count, group_name in enumerate(group_names):
        await _process_group(
            group_name=group_name,
            loaders=loaders,
            progress=count / len(group_names),
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
