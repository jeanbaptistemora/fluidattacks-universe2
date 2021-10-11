#!/usr/bin/env python3
# -.- coding: utf-8 -.-
# pylint: disable=invalid-name,import-error
"""
This migration aims to copy historic_treatment from
finding to vulnerability

Execution Time:    2020-11-26 13:42:51 UTC-5
Finalization Time: 2020-11-26 14:19:55 UTC-5
"""

from aioextensions import (
    collect,
    run,
)
from custom_types import (
    Finding,
)
from dataloaders.finding import (
    FindingLoader,
)
from dataloaders.group import (
    GroupLoader,
)
from groups.domain import (
    get_active_groups,
)
from itertools import (
    chain,
)
from more_itertools import (
    chunked,
)
from newutils.datetime import (
    DEFAULT_STR,
    get_from_str,
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
    add_vulnerability_treatment,
    list_vulnerabilities_async,
)

STAGE: str = os.environ["STAGE"]


async def _copy_historic_treatment(  # noqa: MC0001
    finding_id: str,
    finding: Dict[str, Finding],
    vuln: Dict[str, Finding],
) -> None:
    historic_treatment = finding.get("historic_treatment", [])
    vuln_historic_treatment = vuln.get("historic_treatment", [])
    treatment_manager = vuln.get("treatment_manager", "")
    vuln_id = str(vuln.get("UUID", ""))
    if vuln_historic_treatment:
        if historic_treatment:
            current_treatment = historic_treatment[-1]
            current_vuln = vuln_historic_treatment[-1]
            if get_from_str(
                current_treatment.get("date", DEFAULT_STR)
            ) > get_from_str(current_vuln.get("date", DEFAULT_STR)):
                if STAGE == "apply":
                    if treatment_manager:
                        current_treatment[
                            "treatment_manager"
                        ] = treatment_manager
                    await add_vulnerability_treatment(
                        finding_id=finding_id,
                        updated_values=current_treatment,
                        vuln=vuln,
                        user_email=current_treatment.get("user", ""),
                        date=current_treatment.get("date", DEFAULT_STR),
                    )
                else:
                    print(
                        f"treatment on finding {finding_id} is most recent"
                        f" than treatment on vuln {vuln_id}"
                    )
            else:
                if (
                    treatment_manager
                    and "treatment_manager" not in current_vuln
                ):
                    if STAGE == "apply":
                        vuln_historic_treatment[-1][
                            "treatment_manager"
                        ] = treatment_manager
                        await vulns_dal.update(
                            finding_id,
                            vuln_id,
                            {"historic_treatment": historic_treatment},
                        )
                    else:
                        print(
                            f"historic_treatment on vuln {vuln_id} without"
                            "treatment_manager"
                        )
    elif historic_treatment:
        if treatment_manager:
            historic_treatment[-1]["treatment_manager"] = treatment_manager
        if STAGE == "apply":
            await vulns_dal.update(
                finding_id, vuln_id, {"historic_treatment": historic_treatment}
            )
        else:
            print(f"vuln {vuln_id} without historic_treatment")


async def copy_historic_treatment(groups: List[str]) -> None:
    groups_data = await GroupLoader().load_many(groups)
    findings_ids = list(
        chain.from_iterable(
            group_data["findings"] for group_data in groups_data
        )
    )
    findings = await FindingLoader().load_many(findings_ids)
    for finding in findings:
        finding_id: str = str(finding.get("finding_id"))
        vulns = await list_vulnerabilities_async([finding_id])
        await collect(
            [
                _copy_historic_treatment(finding_id, finding, vuln)
                for vuln in vulns
            ],
            workers=5,
        )


async def main() -> None:
    groups = await get_active_groups()
    await collect(
        [
            copy_historic_treatment(list_group)
            for list_group in chunked(groups, 5)
        ]
    )


if __name__ == "__main__":
    run(main())
