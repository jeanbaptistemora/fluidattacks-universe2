# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from dataloaders import (
    get_new_context,
)
from db_model.forces.types import (
    ForcesExecution,
    GroupForcesExecutionsRequest,
)
from decimal import (
    Decimal,
    ROUND_FLOOR,
)
import math

MAX_WITH_DECIMALS = Decimal("10.0")


async def get_all_time_forces_executions(
    group_name: str,
) -> tuple[ForcesExecution, ...]:
    loaders = get_new_context()
    executions: tuple[
        ForcesExecution, ...
    ] = await loaders.group_forces_executions.load(
        GroupForcesExecutionsRequest(group_name=group_name)
    )

    return executions


def get_finding_name(item: list[str]) -> str:
    return item[0].split("/")[-1]


def format_cvssf_log_adjusted(cvssf: Decimal) -> Decimal:
    cvssf_log: Decimal
    if cvssf == Decimal("0.0"):
        return cvssf.quantize(Decimal("0.1"))

    if abs(cvssf) >= MAX_WITH_DECIMALS:
        cvssf_log = Decimal(
            math.log2(
                abs(cvssf.to_integral_exact(rounding=ROUND_FLOOR))
                * Decimal("10.0")
            )
        )
        return (
            cvssf_log
            if cvssf > Decimal("0.0")
            else cvssf_log * Decimal("-1.0")
        )

    cvssf_log = Decimal(math.log2(abs(cvssf) * Decimal("10.0")))
    return cvssf_log if cvssf > Decimal("0.0") else cvssf_log * Decimal("-1.0")
