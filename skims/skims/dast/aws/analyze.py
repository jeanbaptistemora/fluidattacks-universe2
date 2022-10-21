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
import dast.aws.f070
import dast.aws.f073
import dast.aws.f099
import dast.aws.f109
import dast.aws.f177
import dast.aws.f203
import dast.aws.f246
import dast.aws.f250
import dast.aws.f256
import dast.aws.f257
import dast.aws.f258
import dast.aws.f259
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
    (core_model.FindingEnum.F070, [*dast.aws.f070.CHECKS]),
    (core_model.FindingEnum.F073, [*dast.aws.f073.CHECKS]),
    (core_model.FindingEnum.F099, [*dast.aws.f099.CHECKS]),
    (core_model.FindingEnum.F109, [*dast.aws.f109.CHECKS]),
    (core_model.FindingEnum.F177, [*dast.aws.f177.CHECKS]),
    (core_model.FindingEnum.F203, [*dast.aws.f203.CHECKS]),
    (core_model.FindingEnum.F246, [*dast.aws.f246.CHECKS]),
    (core_model.FindingEnum.F250, [*dast.aws.f250.CHECKS]),
    (core_model.FindingEnum.F256, [*dast.aws.f256.CHECKS]),
    (core_model.FindingEnum.F257, [*dast.aws.f257.CHECKS]),
    (core_model.FindingEnum.F258, [*dast.aws.f258.CHECKS]),
    (core_model.FindingEnum.F259, [*dast.aws.f259.CHECKS]),
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
