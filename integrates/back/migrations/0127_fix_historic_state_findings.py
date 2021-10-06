# pylint: disable=invalid-name
"""
This migration aims to fix the historic state dates used in the creation
of new findings, in the context of the types standarization effort.

The historic state from the original finding is restored to the new one. A
backup from FI_findings table is used for old findings.

Related issue:
https://gitlab.com/fluidattacks/product/-/issues/4903

Execution Time:    2021-08-25 at 15:47:47 UTC-05
Finalization Time: 2021-08-25 at 15:48:29 UTC-05
"""

from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
    run,
)
from boto3.dynamodb.conditions import (
    Key,
)
import csv
from custom_types import (
    Finding as FindingType,
    Historic as HistoricType,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from dynamodb import (
    operations_legacy as dynamodb_ops,
)
from findings import (
    dal as findings_dal,
)
from newutils.utils import (
    duplicate_dict_keys,
)
import time
from typing import (
    Dict,
)

PROD: bool = True

BACKUP_NAME: str = "backup_findings_aug_18"
TABLE_NAME: str = "FI_findings"


def _get_analyst(
    finding: Dict[str, FindingType],
) -> str:
    analyst = ""
    historic_state: HistoricType = finding["historic_state"]
    if historic_state:
        analyst = historic_state[0].get("analyst", "")
    return analyst


def _get_status_date(
    finding: Dict[str, FindingType],
    status_to_search: str,
) -> str:
    date = ""
    historic_state: HistoricType = finding["historic_state"]
    if historic_state:
        dates = [
            state["date"]
            for state in historic_state
            if state["state"] == status_to_search
        ]
        if dates:
            date = max(dates)
    return date


async def _get_finding(
    finding_id: str,
    table_name: str,
) -> Dict[str, FindingType]:
    response = {}
    query_attrs = {
        "KeyConditionExpression": Key("finding_id").eq(finding_id),
        "Limit": 1,
    }
    response_items = await dynamodb_ops.query(table_name, query_attrs)
    if response_items:
        response = response_items[0]
        # Compatibility with old API
        if response["project_name"] is not None:
            response = duplicate_dict_keys(
                response, "group_name", "project_name"
            )
    return response


async def process_finding(
    context: Dataloaders,
    group_name: str,
    finding_name: str,
    old_finding_id: str,
) -> bool:
    # Get target finding
    group_findings_loader: DataLoader = context.group_findings
    group_findings = await group_findings_loader.load(group_name)
    group_findings_titles = [finding["title"] for finding in group_findings]
    finding_id = ""
    if finding_name in group_findings_titles:
        finding_id = next(
            finding["id"]
            for finding in group_findings
            if finding["title"] == finding_name
        )
    else:
        print(f"> ERROR finding {group_name} - {finding_name} NOT found")
        return False

    target_finding = await _get_finding(finding_id, TABLE_NAME)
    target_approved = _get_status_date(target_finding, "APPROVED")

    # Get info from backup finding
    old_finding = await _get_finding(old_finding_id, BACKUP_NAME)

    # Check for unusual conditions
    if len(target_finding["historic_state"]) != 3:
        return True
    if _get_analyst(target_finding) != _get_analyst(old_finding):
        return True
    if target_approved < "2021-08-18 14:15:41":
        return True

    # Update historic in finding
    success = False
    if PROD:
        success = await findings_dal.update(
            finding_id, {"historic_state": old_finding["historic_state"]}
        )
    print(
        f"> info: {group_name}, finding ({finding_id}) <{finding_name}> "
        f", updated??? {success}"
    )
    return success


async def main() -> None:
    # Read findings info
    with open("0120.csv", mode="r", encoding="utf8") as f:
        reader = csv.reader(f)
        info = [
            {
                "group_name": row[0],
                "finding_name": row[1],
                "finding_id": row[2],
            }
            for row in reader
            if "group" not in row[0]
        ]

    context: Dataloaders = get_new_context()
    success = all(
        await collect(
            process_finding(
                context,
                finding["group_name"],
                finding["finding_name"],
                finding["finding_id"],
            )
            for finding in info
        )
    )

    print(f"= success: {success}")


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    print(f"{execution_time}\n{finalization_time}")
