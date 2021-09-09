from charts.colors import (
    RISK,
)
from custom_types import (
    Vulnerability,
)
from decimal import (
    Decimal,
    ROUND_CEILING,
)
from statistics import (
    mean,
)
from typing import (
    Any,
    Dict,
    List,
    NamedTuple,
    Tuple,
)

ORGANIZATION_CATEGORIES: List[str] = [
    "My organization",
    "Average organization",
    "Best organization",
]

GROUP_CATEGORIES: List[str] = [
    "My group",
    "Average group",
    "Best group",
]

PORTFOLIO_CATEGORIES: List[str] = [
    "My portfolio",
    "Average portfolio",
    "Best portfolio",
]


class Benchmarking(NamedTuple):
    is_valid: bool
    mttr: Decimal
    subject: str
    number_of_reattacks: int


def get_vulnerability_reattacks(*, vulnerability: Vulnerability) -> int:
    return sum(
        1
        for verification in vulnerability["historic_verification"]
        if verification.get("status") == "REQUESTED"
    )


def format_data(
    data: Tuple[Decimal, Decimal, Decimal], categories: List[str]
) -> Dict[str, Any]:

    return dict(
        data=dict(
            columns=[
                [
                    "Mean time to remediate",
                    Decimal("0")
                    if data[0] == Decimal("Infinity")
                    else data[0],
                    data[1],
                    data[2],
                ]
            ],
            colors={
                "Mean time to remediate": RISK.neutral,
            },
            labels=True,
            type="bar",
        ),
        axis=dict(
            x=dict(
                categories=categories,
                type="category",
            ),
            y=dict(
                min=0,
                padding=dict(
                    bottom=0,
                ),
                label=dict(
                    text="Calendar days (less is better)",
                    position="inner-top",
                ),
            ),
        ),
        barChartYTickFormat=True,
    )


def get_valid_organizations(
    *,
    organizations: Tuple[Benchmarking, ...],
    subject: str,
) -> List[Benchmarking]:
    return [
        organization
        for organization in organizations
        if subject != organization.subject
        and organization.is_valid
        and organization.mttr != Decimal("Infinity")
    ]


def get_mean_organizations(*, organizations: List[Benchmarking]) -> Decimal:
    return (
        Decimal(
            mean([organization.mttr for organization in organizations])
        ).to_integral_exact(rounding=ROUND_CEILING)
        if organizations
        else Decimal("0")
    )


def get_best_mttr(*, organizations: List[Benchmarking]) -> Decimal:
    return (
        Decimal(
            min([organization.mttr for organization in organizations])
        ).to_integral_exact(rounding=ROUND_CEILING)
        if organizations
        else Decimal("0")
    )
