from aioextensions import (
    collect,
)
from charts.colors import (
    RISK,
)
from charts.utils import (
    get_portfolios_groups,
    iterate_groups,
    iterate_organizations_and_groups,
    json_dump,
)
from custom_types import (
    Vulnerability,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
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
    Awaitable,
    Callable,
    Counter,
    Dict,
    List,
    NamedTuple,
    Tuple,
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


def format_mttr_data(
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
                [column, *[value for _, value in data]],
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


def sum_mttr_many_groups(*, groups_data: Tuple[Remediate, ...]) -> Remediate:

    return Remediate(
        critical_severity=Decimal(
            mean([group.critical_severity for group in groups_data])
        )
        .quantize(Decimal("0.1"))
        .to_integral_exact(rounding=ROUND_CEILING)
        if groups_data
        else Decimal("0"),
        high_severity=Decimal(
            mean([group.high_severity for group in groups_data])
        )
        .quantize(Decimal("0.1"))
        .to_integral_exact(rounding=ROUND_CEILING)
        if groups_data
        else Decimal("0"),
        medium_severity=Decimal(
            mean([group.medium_severity for group in groups_data])
        )
        .quantize(Decimal("0.1"))
        .to_integral_exact(rounding=ROUND_CEILING)
        if groups_data
        else Decimal("0"),
        low_severity=Decimal(
            mean([group.low_severity for group in groups_data])
        )
        .quantize(Decimal("0.1"))
        .to_integral_exact(rounding=ROUND_CEILING)
        if groups_data
        else Decimal("0"),
    )


async def generate_all_top_vulnerabilities(
    *,
    get_data_one_group: Callable[[str, Dataloaders], Awaitable[Counter[str]]],
    get_data_many_groups: Callable[
        [List[str], Dataloaders], Awaitable[Counter[str]]
    ],
    format_data: Callable[[Counter[str]], Dict[str, Any]],
) -> None:
    loaders = get_new_context()
    async for group in iterate_groups():
        json_dump(
            document=format_data(
                await get_data_one_group(group, loaders),
            ),
            entity="group",
            subject=group,
        )

    async for org_id, _, org_groups in (iterate_organizations_and_groups()):
        json_dump(
            document=format_data(
                await get_data_many_groups(list(org_groups), loaders),
            ),
            entity="organization",
            subject=org_id,
        )

    async for org_id, org_name, _ in (iterate_organizations_and_groups()):
        for portfolio, groups in await get_portfolios_groups(org_name):
            json_dump(
                document=format_data(
                    await get_data_many_groups(list(groups), loaders),
                ),
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
            )
