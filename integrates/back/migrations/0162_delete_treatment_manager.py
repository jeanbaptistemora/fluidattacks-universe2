# pylint: disable=invalid-name
"""
This migration aims to delete treatment_manager after a related
migration that copy that data to assigned be executed.

Execution Time:
Finalization Time:
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

PROD: bool = False


async def delete_treatment_manager(*, vulnerability: Dict[str, Any]) -> None:
    historic_treatment: List[Dict[str, str]] = vulnerability[
        "historic_treatment"
    ]
    if historic_treatment is None:
        return

    new_historic_treatment: List[Dict[str, str]] = copy.deepcopy(
        historic_treatment
    )
    should_update: bool = False
    for treatment in new_historic_treatment:
        if "treatment_manager" in treatment and "assigned" in treatment:
            manager = treatment.get("treatment_manager", "")
            assigned = treatment.get("assigned", "")
            if assigned == manager:
                should_update = True
                del treatment["treatment_manager"]

    if should_update:
        if PROD:
            await update(
                finding_id=str(vulnerability["finding_id"]),
                vuln_id=str(vulnerability["UUID"]),
                data={"historic_treatment": new_historic_treatment},
            )
        else:
            print(
                "Deleting treatment manager in",
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
        tuple(
            delete_treatment_manager(vulnerability=vulnerability)
            for vulnerability in valid_vulnerabilities
            if "historic_treatment" in vulnerability
        ),
        workers=16,
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
