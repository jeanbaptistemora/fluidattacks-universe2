# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from datetime import (
    datetime,
)
from integrates.dal import (
    do_finish_execution,
    do_start_execution,
)
from model import (
    core_model,
)
from typing import (
    Dict,
    Tuple,
    Union,
)

VulnStreamType = Dict[
    core_model.VulnerabilityKindEnum,
    Tuple[
        Union[
            core_model.IntegratesVulnerabilitiesInputs,
            core_model.IntegratesVulnerabilitiesLines,
        ],
        ...,
    ],
]


async def do_finish_skims_execution(
    root: str,
    group_name: str,
    job_id: str,
    end_date: datetime,
    findings_executed: Tuple[Dict[str, Union[int, str]], ...],
) -> bool:
    return await do_finish_execution(
        root=root,
        group_name=group_name,
        job_id=job_id,
        end_date=end_date.isoformat(),
        findings_executed=findings_executed,
    )


async def do_start_skims_execution(
    root: str,
    group_name: str,
    job_id: str,
    start_date: datetime,
    commit_hash: str,
) -> bool:
    return await do_start_execution(
        root=root,
        group_name=group_name,
        job_id=job_id,
        start_date=start_date.isoformat(),
        commit_hash=commit_hash,
    )
