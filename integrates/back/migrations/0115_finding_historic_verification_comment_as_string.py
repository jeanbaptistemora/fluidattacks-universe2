# pylint: disable=invalid-name
"""
This migration change the comment type from integer to string in the finding
historic verification

Execution Time:     2021-08-03 at 09:37:26 UTC-05
Finalization Time:  2021-08-03 at 09:39:14 UTC-05
"""

from aioextensions import (
    collect,
    run,
)
import copy
from custom_types import (  # pylint: disable=import-error
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


async def set_historic_verification_comment_as_string(
    finding: Dict[str, Finding]
) -> bool:
    success = True
    to_update = False
    finding_id = finding["finding_id"]
    old_historic_verification = cast(
        Historic, finding.get("historic_verification", [])
    )
    historic_verification = copy.deepcopy(old_historic_verification)

    for verification_info in historic_verification:
        if type(verification_info["comment"]) != str:  # noqa
            to_update = True
            verification_info["comment"] = str(verification_info["comment"])

    if to_update:
        success = await findings_dal.update(
            finding_id, {"historic_verification": historic_verification}
        )
        print(f"finding_id = {finding_id}")
        print("old_historic_verification =")
        pprint(old_historic_verification)
        print("historic_verification =")
        pprint(historic_verification)

    return success


async def main() -> None:
    scan_attrs = {
        "ProjectionExpression": ",".join(
            {"finding_id", "historic_verification"}
        )
    }
    findings = await dynamodb_ops.scan(FINDING_TABLE, scan_attrs)

    success = all(
        await collect(
            [
                set_historic_verification_comment_as_string(finding)
                for finding in findings
            ]
        )
    )

    print(f"Success: {success}")


if __name__ == "__main__":
    run(main())
