# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# pylint: disable=invalid-name
"""
This migration removes the origin field from finding historic state

Execution Time:    2021-03-01 at 09:57:35 UTC-05
Finalization Time: 2021-03-01 at 10:08:58 UTC-05
"""

from aioextensions import (
    collect,
    run,
)
import copy
from custom_types import (
    Finding,
    Historic,
)
from dynamodb import (
    operations_legacy as dynamodb_ops,
)
from findings import (
    dal as findings_dal,
)
from pprint import (
    pprint,
)
from typing import (
    cast,
    Dict,
)

FINDING_TABLE: str = "FI_findings"


async def remove_origin_from_historic_state(
    finding: Dict[str, Finding]
) -> bool:
    success = True
    to_update = False
    finding_id = finding["finding_id"]
    old_historic_state = cast(Historic, finding.get("historic_state", []))
    historic_state = copy.deepcopy(old_historic_state)

    for state_info in historic_state:
        if state_info.get("origin"):
            to_update = True
            del state_info["origin"]

    if to_update:
        success = await findings_dal.update(
            finding_id, {"historic_state": historic_state}
        )
        print(f"finding_id = {finding_id}")
        print("old_historic_state =")
        pprint(old_historic_state)
        print("historic_state =")
        pprint(historic_state)

    return success


async def main() -> None:
    scan_attrs = {
        "ProjectionExpression": ",".join({"finding_id", "historic_state"})
    }
    findings = await dynamodb_ops.scan(FINDING_TABLE, scan_attrs)

    success = all(
        await collect(
            [
                remove_origin_from_historic_state(finding)
                for finding in findings
            ]
        )
    )

    print(f"Success: {success}")


if __name__ == "__main__":
    run(main())
