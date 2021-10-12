from aioextensions import (
    collect,
)
from async_lru import (
    alru_cache,
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
from groups.domain import (
    get_alive_group_names,
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


@alru_cache(maxsize=None, typed=True)
async def get_data_many_groups_mttr(
    *,
    organization_id: str,
    groups: Tuple[str, ...],
    loaders: Dataloaders,
    get_data_one_group: Callable[[str, Dataloaders], Awaitable[Benchmarking]],
) -> Benchmarking:
    groups_data: Tuple[Benchmarking, ...] = await collect(
        [get_data_one_group(group, loaders) for group in groups]
    )

    mttr: Decimal = (
        Decimal(
            mean([group_data.mttr for group_data in groups_data])
        ).to_integral_exact(rounding=ROUND_CEILING)
        if groups_data
        else Decimal("Infinity")
    )
    number_of_reattacks = sum(
        group_data.number_of_reattacks for group_data in groups_data
    )

    return Benchmarking(
        is_valid=number_of_reattacks > 1000,
        subject=organization_id,
        mttr=mttr,
        number_of_reattacks=number_of_reattacks,
    )


async def generate_all_mttr_benchmarking(  # pylint: disable=too-many-locals
    *,
    get_data_one_group: Callable[[str, Dataloaders], Awaitable[Benchmarking]],
) -> None:
    loaders: Dataloaders = get_new_context()
    organizations: List[Tuple[str, Tuple[str, ...]]] = []
    portfolios: List[Tuple[str, Tuple[str, ...]]] = []
    groups: List[str] = list(
        sorted(await get_alive_group_names(), reverse=True)
    )
    oldest_open_age: Decimal = await get_oldest_open_age(
        groups=groups, loaders=loaders
    )

    async for org_id, _, org_groups in iterate_organizations_and_groups():
        organizations.append((org_id, org_groups))

    async for org_id, org_name, _ in iterate_organizations_and_groups():
        for portfolio, p_groups in await get_portfolios_groups(org_name):
            portfolios.append((portfolio, tuple(p_groups)))

    all_groups_data: Tuple[Benchmarking, ...] = await collect(
        [
            get_data_one_group(
                group,
                loaders,
            )
            for group in groups
        ],
        workers=24,
    )

    all_organizations_data: Tuple[Benchmarking, ...] = await collect(
        [
            get_data_many_groups_mttr(
                organization_id=organization[0],
                groups=organization[1],
                loaders=loaders,
                get_data_one_group=get_data_one_group,
            )
            for organization in organizations
        ],
        workers=24,
    )

    all_portfolios_data: Tuple[Benchmarking, ...] = await collect(
        [
            get_data_many_groups_mttr(
                organization_id=portfolio[0],
                groups=portfolio[1],
                loaders=loaders,
                get_data_one_group=get_data_one_group,
            )
            for portfolio in portfolios
        ],
        workers=24,
    )

    best_mttr = get_best_mttr(
        subjects=[
            organization
            for organization in all_organizations_data
            if organization.is_valid
        ]
    )

    worst_organazation_mttr = get_worst_mttr(
        subjects=[
            organization
            for organization in all_organizations_data
            if organization.is_valid
        ],
        oldest_open_age=oldest_open_age,
    )

    best_group_mttr = get_best_mttr(
        subjects=[group for group in all_groups_data if group.is_valid]
    )

    worst_group_mttr = get_worst_mttr(
        subjects=[group for group in all_groups_data if group.is_valid],
        oldest_open_age=oldest_open_age,
    )

    best_portfolio_mttr = get_best_mttr(
        subjects=[
            portfolio
            for portfolio in all_portfolios_data
            if portfolio.is_valid
        ]
    )

    worst_portfolio_mttr = get_worst_mttr(
        subjects=[
            portfolio
            for portfolio in all_portfolios_data
            if portfolio.is_valid
        ],
        oldest_open_age=oldest_open_age,
    )

    async for group in iterate_groups():
        json_dump(
            document=format_mttr_data(
                data=(
                    Decimal(
                        (
                            await get_data_one_group(
                                group,
                                loaders,
                            )
                        ).mttr
                    ).to_integral_exact(rounding=ROUND_CEILING),
                    best_group_mttr,
                    get_mean_organizations(
                        organizations=get_valid_subjects(
                            all_subjects=all_groups_data,
                            subject=group,
                        )
                    ),
                    worst_group_mttr,
                ),
                categories=GROUP_CATEGORIES,
            ),
            entity="group",
            subject=group,
        )

    async for org_id, _, org_groups in iterate_organizations_and_groups():
        json_dump(
            document=format_mttr_data(
                data=(
                    (
                        await get_data_many_groups_mttr(
                            organization_id=org_id,
                            groups=org_groups,
                            loaders=loaders,
                            get_data_one_group=get_data_one_group,
                        )
                    ).mttr,
                    best_mttr,
                    get_mean_organizations(
                        organizations=get_valid_subjects(
                            all_subjects=all_organizations_data,
                            subject=org_id,
                        )
                    ),
                    worst_organazation_mttr,
                ),
                categories=ORGANIZATION_CATEGORIES,
            ),
            entity="organization",
            subject=org_id,
        )

    async for org_id, org_name, _ in iterate_organizations_and_groups():
        for portfolio, groups in await get_portfolios_groups(org_name):
            json_dump(
                document=format_mttr_data(
                    data=(
                        (
                            await get_data_many_groups_mttr(
                                organization_id=portfolio,
                                groups=tuple(groups),
                                loaders=loaders,
                                get_data_one_group=get_data_one_group,
                            )
                        ).mttr,
                        best_portfolio_mttr,
                        get_mean_organizations(
                            organizations=get_valid_subjects(
                                all_subjects=all_portfolios_data,
                                subject=portfolio,
                            )
                        ),
                        worst_portfolio_mttr,
                    ),
                    categories=PORTFOLIO_CATEGORIES,
                ),
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
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

    async for org_id, _, org_groups in iterate_organizations_and_groups():
        json_dump(
            document=format_data(
                await get_data_many_groups(list(org_groups), loaders),
            ),
            entity="organization",
            subject=org_id,
        )

    async for org_id, org_name, _ in iterate_organizations_and_groups():
        for portfolio, groups in await get_portfolios_groups(org_name):
            json_dump(
                document=format_data(
                    await get_data_many_groups(list(groups), loaders),
                ),
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
            )
