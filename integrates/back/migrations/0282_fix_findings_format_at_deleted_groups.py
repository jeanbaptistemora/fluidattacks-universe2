# pylint: disable=invalid-name
"""
Identify and fix findings with formatting inconsistencies, due to errors
in migrations 0238 and 0239.
These findings were left out as migrations only ran on active groups.

Execution Time:    2022-09-21 at 18:06:24 UTC
Finalization Time: 2022-09-21 at 19:41:33 UTC
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
    PrimaryKey,
)
from organizations.domain import (
    get_all_deleted_groups,
)
import time


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
) -> Item | None:
    item = next(
        (
            item
            for item in milestones_items
            if item["pk"] == f"FIN#{finding_id}#{suffix}"
        ),
        None,
    )

    return (
        None if not item else {k: item[k] for k in item.keys() - {"pk", "sk"}}
    )


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
        "approval": approval,
        "submission": submission,
        "verification": verification,
    }
    item = {key: value for key, value in item.items() if value}
    if not item:
        return

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
    await operations.batch_delete_item(
        keys=tuple(
            PrimaryKey(
                partition_key=item["pk"],
                sort_key=item["sk"],
            )
            for item in milestones_items
        ),
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
