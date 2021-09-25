from aioextensions import (
    collect,
)
from charts.colors import (
    RISK,
)
from context import (
    FI_API_STATUS,
)
from custom_types import (
    Vulnerability,
)
from dataloaders import (
    Dataloaders,
)
from db_model.findings.types import (
    Finding,
)
from decimal import (
    Decimal,
    ROUND_CEILING,
)
from findings.domain.core import (
    get_finding_open_age,
)
from statistics import (
    mean,
)
from typing import (
    Any,
    cast,
    Counter,
    Dict,
    List,
    NamedTuple,
    Tuple,
    Union,
)

ORGANIZATION_CATEGORIES: List[str] = [
    "My organization",
    "Best organization",
    "Average organization",
    "Worst organization",
]

GROUP_CATEGORIES: List[str] = [
    "My group",
    "Best group",
    "Average group",
    "Worst group",
]

PORTFOLIO_CATEGORIES: List[str] = [
    "My portfolio",
    "Best portfolio",
    "Average portfolio",
    "Worst portfolio",
]


Remediate = NamedTuple(
    "Remediate",
    [
        ("critical_severity", Decimal),
        ("high_severity", Decimal),
        ("medium_severity", Decimal),
        ("low_severity", Decimal),
    ],
)


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
    data: Tuple[Decimal, Decimal, Decimal, Decimal],
    categories: List[str],
    y_label: str = "Days per severity (less is better)",
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
                    data[3],
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
                    text=y_label,
                    position="inner-top",
                ),
            ),
        ),
        barChartYTickFormat=True,
    )


def get_valid_subjects(
    *,
    all_subjects: Tuple[Benchmarking, ...],
    subject: str,
) -> List[Benchmarking]:
    return [
        _subject
        for _subject in all_subjects
        if subject != _subject.subject
        and _subject.is_valid
        and _subject.mttr != Decimal("Infinity")
    ]


def get_mean_organizations(*, organizations: List[Benchmarking]) -> Decimal:
    return (
        Decimal(
            mean([organization.mttr for organization in organizations])
        ).to_integral_exact(rounding=ROUND_CEILING)
        if organizations
        else Decimal("0")
    )


def get_best_mttr(*, subjects: List[Benchmarking]) -> Decimal:
    return (
        Decimal(min([subject.mttr for subject in subjects])).to_integral_exact(
            rounding=ROUND_CEILING
        )
        if subjects
        else Decimal("0")
    )


def get_worst_mttr(
    *, subjects: List[Benchmarking], oldest_open_age: Decimal
) -> Decimal:
    valid_subjects = [
        subject for subject in subjects if subject.mttr != Decimal("Infinity")
    ]

    return (
        Decimal(
            max([subject.mttr for subject in valid_subjects])
        ).to_integral_exact(rounding=ROUND_CEILING)
        if valid_subjects
        else oldest_open_age
    )


def format_vulnerabilities_by_data(
    *, counters: Counter[str], column: str, tick_rotation: int, categories: int
) -> Dict[str, Any]:
    data = counters.most_common()[:categories]

    return dict(
        data=dict(
            columns=[
                cast(List[Union[int, str]], [column])
                + [value for _, value in data],
            ],
            colors={
                column: RISK.neutral,
            },
            type="bar",
        ),
        legend=dict(
            position="bottom",
        ),
        axis=dict(
            x=dict(
                categories=[key for key, _ in data],
                type="category",
                tick=dict(
                    rotate=tick_rotation,
                    multiline=False,
                ),
            ),
            y=dict(
                min=0,
                padding=dict(
                    bottom=0,
                ),
            ),
        ),
        barChartYTickFormat=True,
    )


async def _get_oldest_open_age(*, group: str, loaders: Dataloaders) -> Decimal:
    if FI_API_STATUS == "migration":
        group_findings_new_loader = loaders.group_findings_new
        group_findings_new: Tuple[
            Finding, ...
        ] = await group_findings_new_loader.load(group.lower())
        findings_open_age = await collect(
            [
                get_finding_open_age(loaders, finding.id)
                for finding in group_findings_new
            ]
        )
    else:
        group_findings_loader = loaders.group_findings
        group_findings = await group_findings_loader.load(group.lower())
        finding_ids = [
            str(finding["finding_id"]) for finding in group_findings
        ]
        findings_open_age = await collect(
            [
                get_finding_open_age(loaders, finding_id)
                for finding_id in finding_ids
            ]
        )

    return (
        Decimal(max(findings_open_age)).to_integral_exact(
            rounding=ROUND_CEILING
        )
        if findings_open_age
        else Decimal("0.0")
    )


async def get_oldest_open_age(
    *, groups: List[str], loaders: Dataloaders
) -> Decimal:
    oldest_open_age: Tuple[int, ...] = await collect(
        [
            _get_oldest_open_age(group=group, loaders=loaders)
            for group in groups
        ],
        workers=24,
    )

    return (
        Decimal(max(oldest_open_age)).to_integral_exact(rounding=ROUND_CEILING)
        if oldest_open_age
        else Decimal("0.0")
    )
