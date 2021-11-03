# pylint: disable=invalid-name
"""
This migration aims to mask the correct attrs in vulns for removed groups.

Execution Time:
Finalization Time:
"""

from aioextensions import (
    collect,
    run,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from custom_types import (
    Historic as HistoricType,
    Vulnerability as VulnerabilityType,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.findings.types import (
    Finding,
)
from groups import (
    dal as groups_dal,
)
from itertools import (
    chain,
)
import time
from typing import (
    List,
)
from vulnerabilities import (
    domain as vulns_domain,
)

PROD: bool = False
MASKED: str = "Masked"


async def _process_vuln(
    progress: float,
    vuln: VulnerabilityType,
) -> None:
    is_masking_needed: bool = False
    if vuln["specific"] != MASKED or vuln["where"] != MASKED:
        is_masking_needed = True
    historic_treatment: HistoricType = vuln["historic_treatment"]
    for state in historic_treatment:
        if (
            "treatment_manager" in state
            and state["treatment_manager"] != MASKED
        ):
            is_masking_needed = True
        if "justification" in state and state["justification"] != MASKED:
            is_masking_needed = True

    if is_masking_needed:
        if PROD:
            success = await vulns_domain.mask_vuln(vuln)
            print(
                f"{progress:.4f},"
                f',MASK,{vuln["finding_id"]},{vuln["UUID"]},{str(success)}'
            )
        else:
            print(
                f"{progress:.4f},"
                f'PENDING,{vuln["finding_id"]},{vuln["UUID"]},{False}'
            )


async def main() -> None:
    loaders: Dataloaders = get_new_context()

    filtering_exp = (
        Attr("project_status").eq("DELETED")
        | Attr("project_status").eq("FINISHED")
        | Attr("project_status").eq("PENDING_DELETION")
    )
    masked_groups = sorted(
        [
            group["project_name"]
            for group in await groups_dal.get_all(filtering_exp=filtering_exp)
        ]
    )
    print(f"Masked groups: {len(masked_groups)}")

    masked_groups = masked_groups[:10]

    findings: List[Finding] = list(
        chain.from_iterable(
            await loaders.group_drafts_and_findings.load_many(masked_groups)
        )
    )
    print(f"Findings: {len(findings)}")

    vulns: List[VulnerabilityType] = list(
        chain.from_iterable(
            await loaders.finding_vulns_all.load_many(
                [finding.id for finding in findings]
            )
        )
    )
    print(f"Vulns: {len(vulns)}")

    await collect(
        _process_vuln(
            progress=count / len(vulns),
            vuln=vuln,
        )
        for count, vuln in enumerate(vulns)
    )

    print("Done!")


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:     %Y-%m-%d at %H:%M:%S %Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time:  %Y-%m-%d at %H:%M:%S %Z"
    )
    print(f"{execution_time}\n{finalization_time}")
