from dataloaders import (
    get_new_context,
)
from db_model.forces.types import (
    ForcesExecution,
    GroupForcesExecutionsRequest,
)
from decimal import (
    Decimal,
    ROUND_CEILING,
    ROUND_FLOOR,
)
import math
import os

MAX_WITH_DECIMALS: Decimal = Decimal("10.0")
BAR_RATIO_WIDTH: Decimal = Decimal("0.4")

try:
    CRITERIA_VULNERABILITIES: str = os.environ[
        "CHARTS_CRITERIA_VULNERABILITIES"
    ]
except KeyError as exe:
    print("Environment variable " + exe.args[0] + " doesn't exist")
    raise


async def get_all_time_forces_executions(
    group_name: str,
) -> list[ForcesExecution]:
    loaders = get_new_context()
    return await loaders.group_forces_executions.load(
        GroupForcesExecutionsRequest(group_name=group_name)
    )


def get_finding_name(item: list[str]) -> str:
    return item[0].split("/")[-1]


def format_cvssf_log_adjusted(cvssf: Decimal) -> Decimal:
    cvssf_log: Decimal
    if cvssf == Decimal("0.0"):
        return cvssf.quantize(Decimal("0.1"))

    if abs(cvssf) >= MAX_WITH_DECIMALS:
        cvssf_log = Decimal(
            math.log2(
                abs(cvssf.to_integral_exact(rounding=ROUND_CEILING))
                * Decimal("10.0")
            )
        )
        if cvssf < Decimal("0.0"):
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


def round_to_next_multiple(*, value: Decimal, base: Decimal) -> Decimal:
    format_value = value.to_integral_exact(rounding=ROUND_CEILING)
    divided = format_value // base
    nearest_multiple = divided * base
    if nearest_multiple > format_value:
        return nearest_multiple

    return nearest_multiple + base


def get_max_axis(*, value: Decimal) -> Decimal:
    if value <= Decimal("100.0"):
        return round_to_next_multiple(value=value, base=Decimal("5.0"))

    exp = Decimal(math.log10(value)).to_integral_exact(rounding=ROUND_CEILING)
    return round_to_next_multiple(
        value=value,
        base=Decimal(math.pow(Decimal("10.0"), exp)).quantize(Decimal("0.1"))
        / Decimal("20.0"),
    )
