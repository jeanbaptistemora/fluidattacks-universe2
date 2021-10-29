# pylint: disable=invalid-name
"""
This migration aims to fix the state milestones for findings.

Findings migrated from FI_findings, had their historic state populated via a
collect, which introduced some inconsistencies for historics with several
SUBMISSION states.

Execution Time:
Finalization Time:
"""

from aioextensions import (
    collect,
    run,
)
from boto3.dynamodb.conditions import (
    Attr,
    Key,
)
from copy import (
    deepcopy,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model import (
    TABLE,
)
from db_model.findings.types import (
    Finding,
)
from dynamodb import (
    keys,
    operations,
)
from dynamodb.exceptions import (
    ConditionalCheckFailedException,
)
from dynamodb.types import (
    Item,
    PrimaryKey,
)
from groups import (
    dal as groups_dal,
)
from itertools import (
    chain,
)
from newutils.datetime import (
    get_as_utc_iso_format,
    get_plus_delta,
)
import time
from typing import (
    List,
)

PROD: bool = False


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


async def _update_state_item(
    state: Item,
    check_if_exists: bool = True,
) -> None:
    primary_key = PrimaryKey(
        partition_key=state.pop("pk"), sort_key=state.pop("sk")
    )
    key_structure = TABLE.primary_key
    condition_expression = (
        Attr(key_structure.partition_key).not_exists()
        & Attr(key_structure.sort_key).not_exists()
    )
    if PROD:
        try:
            await operations.update_item(
                condition_expression=condition_expression
                if check_if_exists
                else None,
                item=state,
                key=primary_key,
                table=TABLE,
            )
            success = True
        except ConditionalCheckFailedException:
            success = False
        print(f'_PROCESSED,{primary_key},{state["status"]},{success}')
    else:
        print(f'_PENDING,{primary_key},{state["status"]},{False}')


async def _fix_submitted_state_missing(historic_state: List[Item]) -> None:
    approval = next(
        (
            state
            for state in reversed(historic_state)
            if state["status"] == "APPROVED"
        ),
        None,
    )
    if not approval:
        return

    submission = next(
        (
            state
            for state in reversed(historic_state)
            if state["status"] == "SUBMITTED"
        ),
        None,
    )
    if submission:
        return

    creation = next(
        state for state in historic_state if state["status"] == "CREATED"
    )
    submission = deepcopy(creation)
    submission["modified_date"] = get_as_utc_iso_format(
        get_plus_delta(
            datetime.fromisoformat(creation["modified_date"]),
            milliseconds=500,
        )
    )
    submission["status"] = "SUBMITTED"
    submission["sk"] = f'STATE#{submission["modified_date"]}'
    await _update_state_item(submission)


async def _fix_submission_state_milestone(
    group_name: str,
    historic_state: List[Item],
    milestones: List[Item],
) -> None:
    submission_state = next(
        (
            state
            for state in reversed(historic_state)
            if state["status"] == "SUBMITTED"
        ),
        None,
    )
    if not submission_state:
        return

    submission_milestone = next(
        (
            state
            for state in reversed(milestones)
            if state["status"] == "SUBMITTED"
        ),
        None,
    )

    if (
        submission_milestone
        and submission_state["modified_date"]
        == submission_milestone["modified_date"]
        and submission_state["modified_by"]
        == submission_milestone["modified_by"]
    ):
        return

    submission_state["pk"] = f'{submission_state["pk"]}#SUBMISSION'
    submission_state["sk"] = f"GROUP#{group_name}"
    await _update_state_item(submission_state)


async def _fix_lastest_state_milestone(
    group_name: str,
    historic_state: List[Item],
    milestones: List[Item],
) -> None:
    latest_state = historic_state[-1]

    latest_milestone = next(
        (
            state
            for state in milestones
            if state["pk"] == f'{latest_state["pk"]}#STATE'
        ),
        None,
    )

    if (
        latest_milestone
        and latest_state["status"] == latest_milestone["status"]
        and latest_state["modified_date"] == latest_milestone["modified_date"]
        and latest_state["modified_by"] == latest_milestone["modified_by"]
    ):
        return

    latest_state["pk"] = f'{latest_state["pk"]}#STATE'
    latest_state["sk"] = f"GROUP#{group_name}"
    await _update_state_item(latest_state, check_if_exists=False)


async def _proccess_finding(
    finding: Finding,
) -> None:
    finding_id: str = finding.id
    group_name: str = finding.group_name

    # Fix finding_historic_state facet
    states = await _get_finding_historic_states(finding_id)
    await _fix_submitted_state_missing(states)

    # Fix finding_submission facet
    states = await _get_finding_historic_states(finding_id)
    milestones = await _get_finding_milestones(group_name, finding_id)
    await _fix_submission_state_milestone(group_name, states, milestones)

    # Fix finding_state facet
    await _fix_lastest_state_milestone(group_name, states, milestones)


async def main() -> None:
    loaders: Dataloaders = get_new_context()

    group_names = [
        group["project_name"] for group in await groups_dal.get_alive_groups()
    ]
    print(f"Alive groups: {len(group_names)}")

    findings: List[Finding] = list(
        chain.from_iterable(
            await loaders.group_findings.load_many(group_names)
        )
    )
    print(f"   === findings: {len(findings)}")

    drafts: List[Finding] = list(
        chain.from_iterable(await loaders.group_drafts.load_many(group_names))
    )
    print(f"   === drafts: {len(drafts)}")

    findings.extend(drafts)
    print(f"   === findings + drafts: {len(findings)}")

    await collect(_proccess_finding(finding) for finding in findings)

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
