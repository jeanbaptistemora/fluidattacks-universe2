# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# pylint: disable=invalid-name,import-error
"""
This migration aims to remove treatment manager when treatment is NEW

Execution Time: 2020-12-21 06:52:08 UTC-5
Finalization Time: 2020-12-21 07:04:20 UTC-5
"""

from aioextensions import (
    collect,
    run,
)
from custom_types import (  # pylint: disable=import-error
    Finding,
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


async def _remove_treatment_manager(vuln: Dict[str, Finding]) -> None:
    finding_id: str = str(vuln["finding_id"])
    vuln_id: str = str(vuln["UUID"])
    should_update: bool = False

    historic_treatment = vuln["historic_treatment"]
    for treatment in historic_treatment:
        if (
            treatment["treatment"] == "NEW"
            and "treatment_manager" in treatment
        ):
            should_update = True
            del treatment["treatment_manager"]

    if should_update:
        if STAGE == "apply":
            await vulns_dal.update(
                finding_id, vuln_id, {"historic_treatment": historic_treatment}
            )
        else:
            print(f"should remove treatment_manager from {vuln_id}")


async def remove_treatment_manager(groups: List[str]) -> None:
    groups_data = await GroupLoader().load_many(groups)
    findings_ids = list(
        chain.from_iterable(
            group_data["findings"] + group_data["drafts"]
            for group_data in groups_data
        )
    )
    vulns = await list_vulnerabilities_async(
        findings_ids,
        include_confirmed_zero_risk=True,
        include_requested_zero_risk=True,
    )
    await collect(
        [_remove_treatment_manager(vuln) for vuln in vulns], workers=5
    )


async def main() -> None:
    groups = await get_active_groups()
    await collect(
        [
            remove_treatment_manager(list_group)
            for list_group in chunked(groups, 5)
        ],
        workers=10,
    )


if __name__ == "__main__":
    run(main())
