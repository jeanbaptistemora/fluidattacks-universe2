# type: ignore

# -.- coding: utf-8 -.-
# pylint: disable=invalid-name
"""
This migration aims to copy external_bts from
finding to vulnerability

Execution Time:    2020-11-12 13:22:45 UTC-5
Finalization Time: 2020-11-12 13:31:12 UTC-5
"""

from aioextensions import (
    collect,
    run,
)
from custom_types import (  # pylint: disable=import-error
    Finding,
)
from dataloaders import (
    get_new_context,
)
from findings.domain import (
    get_findings_async,
    list_findings,
)
from groups.domain import (
    get_active_groups,
)
from more_itertools import (
    chunked,
)
import os
from typing import (
    Dict,
    List,
)
from vulnerabilities import (
    dal as vulns_dal,
)
from vulnerabilities.domain import (
    list_vulnerabilities_async,
)

STAGE: str = os.environ["STAGE"]


async def _copy_external_bts(
    finding_id: str,
    finding: Dict[str, Finding],
    vuln: Dict[str, Finding],
) -> None:
    external_bts = finding.get("externalBts", "")
    vuln_external_bts = vuln.get("external_bts", "")
    vuln_id = str(vuln.get("UUID", ""))
    if external_bts and not vuln_external_bts:
        if STAGE == "apply":
            await vulns_dal.update(
                finding_id, vuln_id, {"external_bts": external_bts}
            )


async def copy_external_bts(groups: List[str]) -> None:
    findings_id = await list_findings(get_new_context(), groups)
    findings = await get_findings_async(
        finding_id
        for finding_group in findings_id
        for finding_id in finding_group
    )
    for finding in findings:
        finding_id: str = str(finding.get("findingId"))
        vulns = await list_vulnerabilities_async([finding_id])
        await collect(
            [_copy_external_bts(finding_id, finding, vuln) for vuln in vulns],
            workers=10,
        )


async def main() -> None:
    groups = await get_active_groups()
    await collect(
        [copy_external_bts(list_group) for list_group in chunked(groups, 10)]
    )


if __name__ == "__main__":
    run(main())
