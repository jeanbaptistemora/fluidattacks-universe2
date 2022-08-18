from aioextensions import (
    collect,
)
from concurrent.futures import (
    ThreadPoolExecutor,
)
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
    Dict,
    List,
)

CHECKS = (
    *dast.aws.f024.CHECKS,
    *dast.aws.f031.CHECKS,
)


async def analyze(
    *,
    credentials: AwsCredentials,
    stores: Dict[core_model.FindingEnum, EphemeralStore],
) -> None:

    vulnerabilities: List[Vulnerability] = list(
        collapse(
            await collect([check(credentials) for check in CHECKS]),
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
