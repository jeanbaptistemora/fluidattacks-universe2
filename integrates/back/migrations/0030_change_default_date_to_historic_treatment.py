# pylint: disable=invalid-name,import-error
"""
This migration changes dafault date to those finding historic_treatments that
have 0001-01-01 00:00:00 as dafault date.
Execution Time:    2020-10-05 15:26:48 UTC-5
Finalization Time: 2020-10-05 16:08:42 UTC-5
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
        finding_id = finding["finding_id"]
        project_name = finding.get("project_name", "")
        historic_treatment = finding.get("historic_treatment", [])
        old_historic_treatment = copy.deepcopy(historic_treatment)
        to_update = False

        for treatment_info in historic_treatment:
            if "date" in treatment_info:
                if treatment_info["date"] == "0001-01-01 00:00:00":
                    treatment_info["date"] = "2000-01-01 00:00:00"
                    to_update = True

        if to_update:
            success = await update(
                finding_id, {"historic_treatment": historic_treatment}
            )
            print("old_historic_treatment =")
            pprint(old_historic_treatment)
            print("historic_treatment =")
            pprint(historic_treatment)
            print(
                f"{project_name} & fin {finding_id} - "
                f"historic_treatment / Success: {success}"
            )


if __name__ == "__main__":
    run(main())
