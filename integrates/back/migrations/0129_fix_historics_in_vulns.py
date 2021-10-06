# pylint: disable=invalid-name
"""
This migration aims to fix the historic state dates of moved vulns,
in the context of the types standarization effort.

The historic state from the original vuln is restored using a restored backup
table.

The oiginal historic state got damaged once the related new draft was approved.

Related issue:
https://gitlab.com/fluidattacks/product/-/issues/4903

Execution Time:    2021-08-27 at 09:59:26 UTC-05
Finalization Time: 2021-08-27 at 10:27:13 UTC-05
"""

from aioextensions import (
    collect,
    run,
)
from boto3.dynamodb.conditions import (
    Key,
)
import csv
from custom_types import (
    Historic as HistoricType,
    Vulnerability as VulnerabilityType,
)
from dynamodb import (
    operations_legacy as dynamodb_ops,
)
from itertools import (
    zip_longest,
)
import time
from typing import (
    Dict,
)
from vulnerabilities import (
    dal as vulns_dal,
)

PROD: bool = True

BACKUP_NAME: str = "backup_vulns_aug_08"
TABLE_NAME: str = "FI_vulnerabilities"


def _replace_historic_dates(
    target_state: HistoricType,
    backup_state: HistoricType,
) -> HistoricType:
    if backup_state:
        date_to_replace = target_state[0]["date"]
    corrected_historic = []
    for state, backup in zip_longest(target_state, backup_state):
        if backup and state["date"] == date_to_replace:
            state["date"] = backup["date"]
        corrected_historic.append(state)
    return corrected_historic


async def _get_vuln(
    uuid: str, table_name: str
) -> Dict[str, VulnerabilityType]:
    response = {}
    hash_key = "UUID"
    query_attrs = {
        "IndexName": "gsi_uuid",
        "KeyConditionExpression": Key(hash_key).eq(uuid),
        "Limit": 1,
    }
    response_items = await dynamodb_ops.query(table_name, query_attrs)
    if response_items:
        response = response_items[0]
    return response


async def process_vuln(uuid: str) -> bool:
    # Get current vuln
    target_vuln = await _get_vuln(uuid, TABLE_NAME)
    if not target_vuln:
        print(f' - ERROR "{uuid}" target vuln NOT found')
        return False

    # Get backup vuln
    backup_vuln = await _get_vuln(uuid, BACKUP_NAME)
    if not backup_vuln:
        print(f' - ERROR "{uuid}" backup vuln NOT found')
        return False

    # Check if the first date is consistent
    if (
        target_vuln["historic_state"][0]["date"]
        == backup_vuln["historic_state"][0]["date"]
    ):
        return True

    # Fix historic state
    historic_state = _replace_historic_dates(
        target_vuln["historic_state"],
        backup_vuln["historic_state"],
    )

    # Fix historic treatment
    historic_treatment = _replace_historic_dates(
        target_vuln.get("historic_treatment", []),
        backup_vuln.get("historic_treatment", []),
    )

    success = False
    if PROD:
        success = await vulns_dal.update(
            target_vuln["finding_id"],
            target_vuln["UUID"],
            {
                "historic_state": historic_state,
                "historic_treatment": historic_treatment,
            },
        )
    print(f' = "{uuid}" historics corrected: {success}')
    return success


async def main() -> None:
    # Read findings info
    with open("0119.csv", mode="r", encoding="utf8") as f:
        reader = csv.reader(f)
        uuids = [row[3] for row in reader if "group" not in row[0]]
    print(f" = uuids({len(uuids)}): {uuids[:3]}")

    success = all(await collect(process_vuln(uuid) for uuid in uuids))

    print(f" = success: {success}")


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    print(f"{execution_time}\n{finalization_time}")
