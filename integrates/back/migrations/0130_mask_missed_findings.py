# pylint: disable=invalid-name
"""
This migration aims to mask some attributes present in several
findings of groups that were deleted

Related issue:
https://gitlab.com/fluidattacks/product/-/issues/5244

Execution Time:    2021-08-31 at 09:55:08 UTC-05
Finalization Time: 2021-08-31 at 09:55:09 UTC-05
"""


from aioextensions import (
    collect,
    run,
)
import csv
from findings import (
    dal as findings_dal,
)
from newutils import (
    findings as findings_utils,
)
import time

PROD: bool = True


async def mask_finding(finding_id: str) -> bool:
    finding = await findings_dal.get_finding(finding_id)
    finding = findings_utils.format_data(finding)
    attrs_to_mask = [
        "affected_systems",
        "attack_vector_desc",
        "effect_solution",
        "related_findings",
        "risk",
        "threat",
        "treatment",
        "treatment_manager",
        "vulnerability",
        "records",
    ]
    success = False
    if PROD:
        print(f"Working on finding with finding_id: {finding_id}")
        success = await findings_dal.update(
            finding_id, {attr: "Masked" for attr in attrs_to_mask}
        )
    return success


async def main() -> None:
    # Read findings to mask
    with open("0130.csv", mode="r", encoding="utf8") as csv_file:
        reader = csv.reader(csv_file)
        finding_ids = [row[0] for row in reader]
    print(f"The findings to mask are: {finding_ids}")
    success = all(
        await collect(mask_finding(finding_id) for finding_id in finding_ids)
    )
    print(f"Success: {success}")


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    print(f"{execution_time}\n{finalization_time}")
