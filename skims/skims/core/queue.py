# Standard library
import asyncio
from typing import (
    List,
)

# Third party libraries
from aioextensions import (
    collect,
)

# Local libraries
from model import (
    core_model,
)
from utils.ctx import (
    PROCESS_GROUP_ON_AWS,
)
from utils.system import (
    call,
)


async def process_group_on_aws(
    finding: core_model.FindingEnum,
    group: str,
    urgent: bool,
) -> bool:
    process: asyncio.subprocess.Process = await call(
        PROCESS_GROUP_ON_AWS,
        group,
        finding.name,
        env=dict(
            MAKES_COMPUTE_ON_AWS_JOB_QUEUE=(
                "skims_soon" if urgent else "skims_later"
            ),
        ),
        stderr=None,
        stdout=None,
    )

    await process.wait()

    success: bool = process.returncode == 0

    return success


async def main(
    findings: List[core_model.FindingEnum],
    group: str,
    urgent: bool,
) -> bool:
    success: bool = all(
        await collect(
            process_group_on_aws(
                group=group,
                finding=finding,
                urgent=urgent,
            )
            for finding in findings
        )
    )

    return success
