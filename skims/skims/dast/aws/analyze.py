from aioextensions import (
    collect,
)
from concurrent.futures import (
    ThreadPoolExecutor,
)
from ctx import (
    CTX,
)
from dast.aws import (
    f005,
    f016,
    f024,
    f031,
    f070,
    f073,
    f081,
    f099,
    f101,
    f109,
    f165,
    f177,
    f200,
    f203,
    f246,
    f250,
    f256,
    f257,
    f258,
    f259,
    f277,
    f281,
    f325,
    f333,
    f335,
    f363,
    f372,
    f394,
    f396,
    f400,
    f406,
    f407,
)
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
)

CHECKS: tuple[tuple[core_model.FindingEnum, Any], ...] = (
    (core_model.FindingEnum.F005, [*f005.CHECKS]),
    (core_model.FindingEnum.F016, [*f016.CHECKS]),
    (core_model.FindingEnum.F024, [*f024.CHECKS]),
    (core_model.FindingEnum.F031, [*f031.CHECKS]),
    (core_model.FindingEnum.F070, [*f070.CHECKS]),
    (core_model.FindingEnum.F073, [*f073.CHECKS]),
    (core_model.FindingEnum.F081, [*f081.CHECKS]),
    (core_model.FindingEnum.F099, [*f099.CHECKS]),
    (core_model.FindingEnum.F101, [*f101.CHECKS]),
    (core_model.FindingEnum.F109, [*f109.CHECKS]),
    (core_model.FindingEnum.F165, [*f165.CHECKS]),
    (core_model.FindingEnum.F177, [*f177.CHECKS]),
    (core_model.FindingEnum.F200, [*f200.CHECKS]),
    (core_model.FindingEnum.F203, [*f203.CHECKS]),
    (core_model.FindingEnum.F246, [*f246.CHECKS]),
    (core_model.FindingEnum.F250, [*f250.CHECKS]),
    (core_model.FindingEnum.F256, [*f256.CHECKS]),
    (core_model.FindingEnum.F257, [*f257.CHECKS]),
    (core_model.FindingEnum.F258, [*f258.CHECKS]),
    (core_model.FindingEnum.F259, [*f259.CHECKS]),
    (core_model.FindingEnum.F277, [*f277.CHECKS]),
    (core_model.FindingEnum.F281, [*f281.CHECKS]),
    (core_model.FindingEnum.F325, [*f325.CHECKS]),
    (core_model.FindingEnum.F333, [*f333.CHECKS]),
    (core_model.FindingEnum.F335, [*f335.CHECKS]),
    (core_model.FindingEnum.F372, [*f372.CHECKS]),
    (core_model.FindingEnum.F363, [*f363.CHECKS]),
    (core_model.FindingEnum.F394, [*f394.CHECKS]),
    (core_model.FindingEnum.F396, [*f396.CHECKS]),
    (core_model.FindingEnum.F406, [*f406.CHECKS]),
    (core_model.FindingEnum.F400, [*f400.CHECKS]),
    (core_model.FindingEnum.F407, [*f407.CHECKS]),
)


async def analyze(
    *,
    credentials: AwsCredentials,
    stores: dict[core_model.FindingEnum, EphemeralStore],
) -> None:

    vulnerabilities: list[Vulnerability] = list(
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
