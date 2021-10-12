# pylint: disable=invalid-name,import-error
"""
This migration aims to remove cwe field from finding

Execution Time:    2021-07-28 at 22:36:09 UTC-05
Finalization Time: 2021-07-28 at 23:02:38 UTC-05
"""

from aioextensions import (
    collect,
    run,
)
from custom_types import (
    DynamoQuery,
    Finding,
)
from dynamodb.operations_legacy import (
    scan,
)
from findings.dal import (
    update,
)
import time
from typing import (
    Dict,
)

# Constants
PROD: bool = False
TABLE_NAME: str = "FI_findings"


async def update_finding(
    finding: Dict[str, Finding],
) -> None:
    finding_id: str = str(finding["finding_id"])
    data_to_update: Dict[str, Finding] = {"cwe": None}
    if PROD and "cwe" in finding:
        print(
            "Updating finding",
            finding_id,
            finding["cwe"],
            data_to_update,
        )
        await update(finding_id, data_to_update)


async def main() -> None:
    scan_attrs: DynamoQuery = {}
    findings = await scan(TABLE_NAME, scan_attrs)
    await collect(
        [update_finding(finding) for finding in findings], workers=20
    )


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    print(f"{execution_time}\n{finalization_time}")
