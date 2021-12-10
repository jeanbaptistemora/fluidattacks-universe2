# pylint: disable=invalid-name
"""
This migration aims to copy treatment_manager to assigned.

Execution Time:     2021-12-10 at 10:04:54 UTC
Finalization Time:  2021-12-10 at 12:40:59 UTC
"""

from aioextensions import (
    collect,
    run,
)
import copy
from custom_types import (
    DynamoQuery,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.findings.types import (
    Finding,
)
from dynamodb import (
    operations_legacy as dynamodb_ops,
)
from groups.domain import (
    get_alive_group_names,
)
import time
from typing import (
    Any,
    Dict,
    List,
    Set,
    Tuple,
)
from vulnerabilities.dal import (
    update,
)

PROD: bool = True


async def copy_assigned(*, vulnerability: Dict[str, Any]) -> None:
    historic_treatment: List[Dict[str, str]] = vulnerability[
        "historic_treatment"
    ]
    new_historic_treatment: List[Dict[str, str]] = copy.deepcopy(
        historic_treatment
    )
    should_update: bool = False
    if historic_treatment is None:
        return
    for treatment in new_historic_treatment:
        assigned = treatment.get("treatment_manager", "")
        if assigned:
            if treatment.get("assigned", "") != assigned:
                should_update = True
                treatment["assigned"] = assigned

    if should_update:
        if PROD:
            await update(
                finding_id=str(vulnerability["finding_id"]),
                vuln_id=str(vulnerability["UUID"]),
                data={"historic_treatment": new_historic_treatment},
            )
        else:
            print(
                "Copying treatment manager to assigned in",
                vulnerability["UUID"],
                "new historic",
                new_historic_treatment,
                "old",
                historic_treatment,
            )


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    group_names: Tuple[str, ...] = await get_alive_group_names()
    findings: Tuple[
        Finding, ...
    ] = await loaders.group_findings.load_many_chained(group_names)
    findings_ids: Set[str] = set(finding.id for finding in findings)
    scan_attrs: DynamoQuery = {}
    vulnerabilities: List[Dict[str, Any]] = await dynamodb_ops.scan(
        "FI_vulnerabilities", scan_attrs
    )
    valid_vulnerabilities: List[Dict[str, Any]] = [
        vulnerability
        for vulnerability in vulnerabilities
        if str(vulnerability.get("finding_id")) in findings_ids
    ]
    await collect(
        [
            copy_assigned(vulnerability=vulnerability)
            for vulnerability in valid_vulnerabilities
            if "historic_treatment" in vulnerability
        ],
        workers=8,
    )


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:     %Y-%m-%d at %H:%M:%S %Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time:  %Y-%m-%d at %H:%M:%S %Z"
    )
    print(f"{execution_time}\n{finalization_time}")
