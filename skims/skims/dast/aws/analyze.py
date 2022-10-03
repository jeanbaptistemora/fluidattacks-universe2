# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from aioextensions import (
    collect,
)
from concurrent.futures import (
    ThreadPoolExecutor,
)
from ctx import (
    CTX,
)
import dast.aws.f016
import dast.aws.f024
import dast.aws.f031
from model import (
    core_model,
)
from model.core_model import (
    AwsCredentials,
    Vulnerability,
)
from more_itertools import (
    collapse,
)
from os import (
    cpu_count,
)
from state.ephemeral import (
    EphemeralStore,
)
from typing import (
    Any,
    Dict,
    List,
    Tuple,
)

CHECKS: Tuple[Tuple[core_model.FindingEnum, Any], ...] = (
    (core_model.FindingEnum.F016, [*dast.aws.f016.CHECKS]),
    (core_model.FindingEnum.F024, [*dast.aws.f024.CHECKS]),
    (core_model.FindingEnum.F031, [*dast.aws.f031.CHECKS]),
)


async def analyze(
    *,
    credentials: AwsCredentials,
    stores: Dict[core_model.FindingEnum, EphemeralStore],
) -> None:

    vulnerabilities: List[Vulnerability] = list(
        collapse(
            await collect(
                [
                    check(credentials)
                    for finding, checks in CHECKS
                    for check in checks
                    if finding in CTX.config.checks
                ]
            ),
            base_type=Vulnerability,
        )
    )
    with ThreadPoolExecutor(max_workers=cpu_count()) as worker:
        worker.map(
            lambda x: stores[  # pylint: disable=unnecessary-lambda
                x.finding
            ].store(x),
            vulnerabilities,
        )
