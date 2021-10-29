# pylint: disable=invalid-name
"""
This migration aims to fix the source for findings reported by Machine.

The source was incorrectly assigned after the findings migration to the
single table model.

Execution Time:     2021-10-28 at 23:27:11 UTC
Finalization Time:  2021-10-29 at 00:20:00 UTC
"""

from aioextensions import (
    collect,
    run,
)
from boto3.dynamodb.conditions import (
    Key,
)
from custom_exceptions import (
    InvalidSource,
)
from custom_types import (
    DynamoQuery,
    Finding as FindingType,
    Historic as HistoricType,
)
from datetime import (
    datetime,
)
from db_model import (
    TABLE,
)
from db_model.enums import (
    Source,
)
from dynamodb import (
    keys,
    operations,
    operations_legacy as dynamodb_ops,
)
from dynamodb.types import (
    Item,
    PrimaryKey,
)
from groups import (
    dal as groups_dal,
)
import time
from typing import (
    List,
)

FINDING_TABLE: str = "FI_findings"  # Before migration
PROD: bool = True


def _map_source(source: str) -> str:
    source = source.lower()
    if source == "integrates":
        source = "asm"
    elif source == "skims":
        source = "machine"
    if source not in {"asm", "machine", "escape"}:
        raise InvalidSource()
    return source


def _format_source(source: str) -> Source:
    return Source[_map_source(source).upper()]


async def _get_finding_milestones(
    group_name: str,
    finding_id: str,
    is_removed: bool = False,
) -> List[Item]:
    primary_key = keys.build_key(
        facet=TABLE.facets["finding_metadata"],
        values={"group_name": group_name, "id": finding_id},
        is_removed=is_removed,
    )

    index = TABLE.indexes["inverted_index"]
    key_structure = index.primary_key
    results = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.sort_key)
            & Key(key_structure.sort_key).begins_with(
                primary_key.partition_key
            )
        ),
        facets=(
            TABLE.facets["finding_approval"],
            TABLE.facets["finding_creation"],
            TABLE.facets["finding_state"],
            TABLE.facets["finding_submission"],
        ),
        index=index,
        table=TABLE,
    )
    return [item for item in results if "source" in item]


async def _get_finding_historic_states(finding_id: str) -> List[Item]:
    primary_key = keys.build_key(
        facet=TABLE.facets["finding_historic_state"],
        values={"id": finding_id},
    )
    key_structure = TABLE.primary_key
    results = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(TABLE.facets["finding_historic_state"],),
        table=TABLE,
    )
    return [item for item in results if "source" in item]


async def _update_state_source(
    *,
    new_source: Source,
    state: Item,
) -> None:
    key_structure = TABLE.primary_key
    primary_key = PrimaryKey(partition_key=state["pk"], sort_key=state["sk"])
    await operations.update_item(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).eq(primary_key.sort_key)
        ),
        item={"source": new_source.value},
        key=primary_key,
        table=TABLE,
    )


# Some legacy findings did not have a CREATED state
# We are adding it before the historics comparison is done
def _validate_state_created(
    analyst: str,
    historic: HistoricType,
) -> HistoricType:
    current_state = str(historic[0]["state"]).upper()
    if current_state == "CREATED":
        return historic
    creation_state = {
        "date": "",
        "analyst": historic[0].get("analyst", "") or analyst,
        "state": "CREATED",
        "source": historic[0]["source"],
    }
    return [creation_state, *historic]


def _compare_state_sources(
    current_states: List[Item],  # Facet finding_historic_state
    old_historic: HistoricType,
) -> bool:
    for old, current in zip(old_historic, current_states):
        if _map_source(old["source"]) != _map_source(current["source"]):
            return False
    return True


async def _fix_historic_state(
    current_milestones: List[Item],  # Approval, creation, submission, state
    current_states: List[Item],  # Facet finding_historic_state
    old_historic: HistoricType,
) -> None:
    for old, current in zip(old_historic, current_states):
        if _map_source(old["source"]) != _map_source(current["source"]):
            # Fix entry in historic state
            await _update_state_source(
                new_source=_format_source(old["source"]),
                state=current,
            )
    for milestone in current_milestones:
        # Fix milestone
        old_state = next(
            (
                state
                for state in reversed(old_historic)
                if state["state"] == milestone["status"]
                and state["analyst"] == milestone["modified_by"]
            ),
            None,
        )
        if old_state and _map_source(old_state["source"]) != _map_source(
            milestone["source"]
        ):
            await _update_state_source(
                new_source=_format_source(old_state["source"]),
                state=milestone,
            )


async def _proccess_finding(
    old_finding: FindingType,
) -> None:
    finding_id: str = old_finding["finding_id"]
    group_name: str = old_finding["project_name"]

    if "historic_state" not in old_finding:
        print(f"ERROR,{group_name},{finding_id},,no_historic_state")
        return

    old_historic = _validate_state_created(
        old_finding.get("analyst", ""),
        old_finding["historic_state"],
    )

    current_states: List[Item] = await _get_finding_historic_states(finding_id)

    if _compare_state_sources(current_states, old_historic):
        # No update needed
        return

    if PROD:
        # Approval, creation, submission, state
        current_milestones: List[Item] = await _get_finding_milestones(
            group_name, finding_id
        )
        # Also check for REMOVED states
        current_milestones.extend(
            await _get_finding_milestones(group_name, finding_id, True)
        )

        if not current_milestones:
            print(
                f"ERROR,{group_name},{finding_id},"
                f'{old_historic[-1].get("state", "")},not_found'
            )
            return

        await _fix_historic_state(
            current_milestones=current_milestones,
            current_states=current_states,
            old_historic=old_historic,
        )
        print(
            f"OK,{group_name},{finding_id},"
            f'{old_historic[-1].get("state", "")},updated'
        )
        return

    print(
        f"PENDING,{group_name},{finding_id},"
        f'{old_historic[-1].get("state", "")},inconsistency_found'
    )


async def main() -> None:
    start_time = datetime.now()
    scan_attrs: DynamoQuery = {}
    findings = await dynamodb_ops.scan(FINDING_TABLE, scan_attrs)
    print(f"--- scan in {datetime.now() - start_time} ---")
    print(f"Scan findings: {len(findings)}")

    alive_groups = [
        group["project_name"] for group in await groups_dal.get_alive_groups()
    ]
    print(f"Alive groups: {len(alive_groups)}")

    alive_findings = [
        finding
        for finding in findings
        if finding.get("project_name", "") in alive_groups
        and finding.get("project_name", "") != "worcester"
    ]
    print(f"Alive groups findings: {len(alive_findings)}")

    await collect(
        _proccess_finding(old_finding) for old_finding in alive_findings
    )

    print("Done!")


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:     %Y-%m-%d at %H:%M:%S %Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time:  %Y-%m-%d at %H:%M:%S %Z"
    )
    print(f"{execution_time}\n{finalization_time}")
