# pylint: disable=invalid-name,import-error
"""
This migration adds time part to those finding dates that
do not have it.
Execution Time:    2020-09-09 15:31:00 UTC-5
Finalization Time: 2020-09-09 15:48:00 UTC-5
"""

import aioboto3
from asyncio import (
    run,
)
import copy
from dynamodb.operations_legacy import (
    RESOURCE_OPTIONS,
)
from findings.dal import (
    update,
)
import os
from pprint import (
    pprint,
)
from typing import (
    Any,
)

STAGE: str = os.environ["STAGE"]
FINDINGS_TABLE = "FI_findings"


def date_has_time(date: str) -> bool:
    return len(date.split(" ")) == 2


async def scan(*, table_name: str, **options: Any) -> Any:
    async with aioboto3.resource(RESOURCE_OPTIONS) as dynamodb_resource:
        table = await dynamodb_resource.Table(table_name)
        response = await table.scan(**options)
        for elem in response.get("Items", []):
            yield elem

        while "LastEvaluatedKey" in response:
            options["ExclusiveStartKey"] = response["LastEvaluatedKey"]
            response = await table.scan(**options)
            for elem in response.get("Items", []):
                yield elem


async def main() -> None:
    async for finding in scan(table_name=FINDINGS_TABLE):
        if (
            finding.get("finding") == "WIPED"
            or finding.get("affected_systems") == "Masked"
            or "releaseDate" not in finding
        ):
            continue

        finding_id = finding["finding_id"]
        project_name = finding["project_name"]
        release_date = finding["releaseDate"]
        historic_state = finding.get("historic_state", [])
        old_historic_state = copy.deepcopy(historic_state)

        if not date_has_time(release_date):
            finding_updated = await update(
                finding_id, {"release_date": release_date}
            )
            print(f"old release_date = {release_date}")
            release_date += " 00:00:00"
            print(f"release_date = {release_date}")
            print(
                f"{project_name} & fin {finding_id} - "
                f"release_date / Success: {finding_updated}"
            )

        to_update = False
        for state in historic_state:
            if (
                "date" in state
                and state["date"]
                and not date_has_time(state["date"])
            ):
                to_update = True
                state["date"] += " 00:00:00"
        if to_update:
            finding_updated = await update(
                finding_id, {"historic_state": historic_state}
            )
            print("old_historic_state =")
            pprint(old_historic_state)
            print("historic_state =")
            pprint(historic_state)
            print(
                f"{project_name} & fin {finding_id} - "
                f"historic_state / Success: {finding_updated}"
            )


if __name__ == "__main__":
    run(main())
