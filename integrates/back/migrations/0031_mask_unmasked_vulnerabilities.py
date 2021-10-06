# pylint: disable=invalid-name
"""
This migration mask the unmasked vulns reported on chartio.
Execution Time:    2020-10-19 13:20:56 UTC-5
Finalization Time: 2020-10-19 13:21:24 UTC-5
"""

from aioextensions import (
    collect,
)
from asyncio import (
    run,
)
from dataloaders import (
    get_new_context,
)
from findings import (
    domain as findings_domain,
)
import os
from typing import (
    List,
)
from vulnerabilities import (
    domain as vulns_domain,
)

STAGE: str = os.environ["STAGE"]
ENVIRONMENT: str = os.environ["ENVIRONMENT"]


async def main() -> None:
    print("[INFO] starting migration 0031")
    findings: List[str] = []
    if ENVIRONMENT == "development":
        findings = ["560175507"]  # Mock data on JSON for test
    else:
        unmask = open("back/migrations/unmasked.csv", "r", encoding="utf8")
        vulns = unmask.read().split("\n")
        unmask.close()
        findings = list(set(map(lambda x: x.split(",")[1], vulns[1:-1])))
        for finding in findings:
            print(f"[INFO] finding {finding} will be masked")
    if STAGE == "test":
        for finding_id in findings:
            list_vulns = await vulns_domain.list_vulnerabilities_async(
                [finding_id], True
            )
            for vuln in list_vulns:
                print(
                    f'[INFO] vuln with UUID {vuln.get("UUID")} will be masked'
                )
    else:
        are_findings_masked = all(
            await collect(
                findings_domain.mask_finding(get_new_context(), finding_id)
                for finding_id in findings
            )
        )
        if are_findings_masked:
            print("[INFO] Migration successful")
        else:
            print("[ERROR] Migration fails")


if __name__ == "__main__":
    run(main())
