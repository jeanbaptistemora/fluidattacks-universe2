# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from aioextensions import (
    collect,
)
from async_lru import (
    alru_cache,
)
from charts.generators.common.colors import (
    VULNERABILITIES_COUNT,
)
from charts.generators.common.utils import (
    BAR_RATIO_WIDTH,
    get_max_axis,
)
from charts.utils import (
    CsvData,
    get_portfolios_groups,
    get_subject_days,
    iterate_groups,
    iterate_organizations_and_groups,
    json_dump,
)
from custom_exceptions import (
    UnsanitizedInputFound,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    date as datetype,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityVerificationStatus,
)
from db_model.vulnerabilities.types import (
    VulnerabilityVerification,
)
from decimal import (
    Decimal,
    ROUND_CEILING,
)
from findings.domain.core import (
    get_finding_open_age,
)
from newutils.datetime import (
    get_date_from_iso_str,
    get_now_minus_delta,
)
from newutils.validations import (
    validate_sanitized_csv_input,
)
from organizations import (
    domain as orgs_domain,
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
    Optional,
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


def get_vulnerability_reattacks(
    *, historic_verification: Tuple[VulnerabilityVerification, ...]
) -> int:
    return sum(
        1
        for verification in historic_verification
        if verification.status == VulnerabilityVerificationStatus.REQUESTED
    )


def get_vulnerability_reattacks_date(
    *,
    historic_verification: Tuple[VulnerabilityVerification, ...],
    min_date: datetype,
) -> int:
    return sum(
        1
        for verification in historic_verification
        if verification.status == VulnerabilityVerificationStatus.REQUESTED
        and get_date_from_iso_str(verification.modified_date) > min_date
    )


def format_mttr_data(
    data: Tuple[Decimal, Decimal, Decimal, Decimal],
    categories: List[str],
    y_label: str = "Days per unit of exposure (CVSSF)",
) -> Dict[str, Any]:

    max_value: Decimal = list(
        sorted(
            [
                Decimal("0.0")
                if data[0] == Decimal("Infinity")
                else abs(value)
                for value in data
            ],
            reverse=True,
        )
    )[0]
    max_axis_value: Decimal = (
        get_max_axis(value=max_value)
        if max_value > Decimal("0.0")
        else Decimal("0.0")
    )

    return dict(
        data=dict(
            columns=[
                [
                    "Mean time to remediate",
                    Decimal("0")
                    if data[0] == Decimal("Infinity")
                    else data[0].to_integral_exact(rounding=ROUND_CEILING),
                    data[1],
                    data[2],
                    data[3],
                ]
            ],
            colors={
                "Mean time to remediate": "#cc6699",
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
                    top=0,
                ),
                label=dict(
                    text=y_label,
                    position="inner-top",
                ),
                tick=dict(
                    count=5,
                ),
                **(
                    {}
                    if max_axis_value == Decimal("0.0")
                    else dict(max=max_axis_value)
                ),
            ),
        ),
        grid=dict(
            x=dict(
                show=False,
            ),
            y=dict(
                show=True,
            ),
        ),
        bar=dict(
            width=dict(
                ratio=BAR_RATIO_WIDTH,
            ),
        ),
        tooltip=dict(
            show=False,
        ),
        hideYAxisLine=True,
        barChartYTickFormat=True,
        legend=dict(
            show=False,
        ),
        mttrBenchmarking=True,
        hideXTickLine=True,
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


def format_value(data: List[Tuple[str, int]]) -> Decimal:
    if data:
        return Decimal(data[0][1]) if data[0][1] else Decimal("1.0")
    return Decimal("1.0")


def format_vulnerabilities_by_data(
    *,
    counters: Counter[str],
    column: str,
    tick_rotation: int,
    categories: int,
    axis_rotated: bool = False,
) -> Dict[str, Any]:
    data = counters.most_common()[:categories]

    return dict(
        data=dict(
            columns=[
                [column, *[value for _, value in data]],
            ],
            colors={
                column: VULNERABILITIES_COUNT,
            },
            labels=None,
            type="bar",
        ),
        legend=dict(
            show=False,
        ),
        axis=dict(
            rotate=axis_rotated,
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
        maxValue=format_value(data),
        **(
            dict(
                exposureTrendsByCategories=True,
                keepToltipColor=True,
            )
            if axis_rotated
            else {}
        ),
    )


async def _get_oldest_open_age(*, group: str, loaders: Dataloaders) -> Decimal:
    group_findings_loader = loaders.group_findings
    group_findings: Tuple[Finding, ...] = await group_findings_loader.load(
        group.lower()
    )
    findings_open_age = await collect(
        tuple(
            get_finding_open_age(loaders, finding.id)
            for finding in group_findings
        ),
        workers=24,
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
        tuple(
            _get_oldest_open_age(group=group, loaders=loaders)  # type: ignore
            for group in groups
        ),
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
    get_data_one_group: Callable[
        [str, Dataloaders, Optional[datetype]], Awaitable[Benchmarking]
    ],
    min_date: Optional[datetype],
) -> Benchmarking:
    groups_data: Tuple[Benchmarking, ...] = await collect(
        tuple(
            get_data_one_group(group, loaders, min_date) for group in groups
        ),
        workers=24,
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
    get_data_one_group: Callable[
        [str, Dataloaders, Optional[datetype]], Awaitable[Benchmarking]
    ],
    alternative: str,
) -> None:
    loaders: Dataloaders = get_new_context()
    list_days: List[int] = [30, 90]
    dates: List[datetype] = [
        get_now_minus_delta(days=list_days[0]).date(),
        get_now_minus_delta(days=list_days[1]).date(),
    ]
    organizations: List[Tuple[str, Tuple[str, ...]]] = []
    portfolios: List[Tuple[str, Tuple[str, ...]]] = []
    group_names: List[str] = list(
        sorted(
            await orgs_domain.get_all_active_group_names(loaders),
            reverse=True,
        )
    )
    oldest_open_age: Decimal = await get_oldest_open_age(
        groups=group_names, loaders=loaders
    )

    async for org_id, _, org_groups in iterate_organizations_and_groups():
        organizations.append((org_id, org_groups))

    async for org_id, org_name, _ in iterate_organizations_and_groups():
        for portfolio, p_groups in await get_portfolios_groups(org_name):
            portfolios.append(
                (f"{org_id}PORTFOLIO#{portfolio}", tuple(p_groups))
            )

    all_groups_data: Tuple[Benchmarking, ...] = await collect(
        [
            get_data_one_group(
                group_name,
                loaders,
                None,
            )
            for group_name in group_names
        ],
        workers=24,
    )

    all_groups_data_30: Tuple[Benchmarking, ...] = await collect(
        [
            get_data_one_group(group_name, loaders, dates[0])
            for group_name in group_names
        ],
        workers=24,
    )

    all_groups_data_90: Tuple[Benchmarking, ...] = await collect(
        [
            get_data_one_group(group_name, loaders, dates[1])
            for group_name in group_names
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
                min_date=None,
            )
            for organization in organizations
        ],
        workers=24,
    )

    all_organizations_data_30: Tuple[Benchmarking, ...] = await collect(
        [
            get_data_many_groups_mttr(
                organization_id=organization[0],
                groups=organization[1],
                loaders=loaders,
                get_data_one_group=get_data_one_group,
                min_date=dates[0],
            )
            for organization in organizations
        ],
        workers=24,
    )

    all_organizations_data_90: Tuple[Benchmarking, ...] = await collect(
        [
            get_data_many_groups_mttr(
                organization_id=organization[0],
                groups=organization[1],
                loaders=loaders,
                get_data_one_group=get_data_one_group,
                min_date=dates[1],
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
                min_date=None,
            )
            for portfolio in portfolios
        ],
        workers=24,
    )

    all_portfolios_data_30: Tuple[Benchmarking, ...] = await collect(
        [
            get_data_many_groups_mttr(
                organization_id=portfolio[0],
                groups=portfolio[1],
                loaders=loaders,
                get_data_one_group=get_data_one_group,
                min_date=dates[0],
            )
            for portfolio in portfolios
        ],
        workers=24,
    )

    all_portfolios_data_90: Tuple[Benchmarking, ...] = await collect(
        [
            get_data_many_groups_mttr(
                organization_id=portfolio[0],
                groups=portfolio[1],
                loaders=loaders,
                get_data_one_group=get_data_one_group,
                min_date=dates[1],
            )
            for portfolio in portfolios
        ],
        workers=24,
    )

    best_mttr: Dict[str, Decimal] = {
        "best_mttr": get_best_mttr(
            subjects=[
                organization
                for organization in all_organizations_data
                if organization.is_valid
            ]
        ),
        "best_mttr_30": get_best_mttr(
            subjects=[
                organization
                for organization in all_organizations_data_30
                if organization.is_valid
            ]
        ),
        "best_mttr_90": get_best_mttr(
            subjects=[
                organization
                for organization in all_organizations_data_90
                if organization.is_valid
            ]
        ),
    }

    worst_organazation_mttr: Dict[str, Decimal] = {
        "worst_organazation_mttr": get_worst_mttr(
            subjects=[
                organization
                for organization in all_organizations_data
                if organization.is_valid
            ],
            oldest_open_age=oldest_open_age,
        ),
        "worst_organazation_mttr_30": get_worst_mttr(
            subjects=[
                organization
                for organization in all_organizations_data_30
                if organization.is_valid
            ],
            oldest_open_age=Decimal("30.0"),
        ),
        "worst_organazation_mttr_90": get_worst_mttr(
            subjects=[
                organization
                for organization in all_organizations_data_90
                if organization.is_valid
            ],
            oldest_open_age=Decimal("90.0"),
        ),
    }

    best_group_mttr: Dict[str, Decimal] = {
        "best_group_mttr": get_best_mttr(
            subjects=[group for group in all_groups_data if group.is_valid]
        ),
        "best_group_mttr_30": get_best_mttr(
            subjects=[group for group in all_groups_data_30 if group.is_valid]
        ),
        "best_group_mttr_90": get_best_mttr(
            subjects=[group for group in all_groups_data_90 if group.is_valid]
        ),
    }

    worst_group_mttr: Dict[str, Decimal] = {
        "worst_group_mttr": get_worst_mttr(
            subjects=[group for group in all_groups_data if group.is_valid],
            oldest_open_age=oldest_open_age,
        ),
        "worst_group_mttr_30": get_worst_mttr(
            subjects=[group for group in all_groups_data_30 if group.is_valid],
            oldest_open_age=Decimal("30.0"),
        ),
        "worst_group_mttr_90": get_worst_mttr(
            subjects=[group for group in all_groups_data_90 if group.is_valid],
            oldest_open_age=Decimal("90.0"),
        ),
    }

    best_portfolio_mttr: Dict[str, Decimal] = {
        "best_portfolio_mttr": get_best_mttr(
            subjects=[
                portfolio
                for portfolio in all_portfolios_data
                if portfolio.is_valid
            ]
        ),
        "best_portfolio_mttr_30": get_best_mttr(
            subjects=[
                portfolio
                for portfolio in all_portfolios_data_30
                if portfolio.is_valid
            ]
        ),
        "best_portfolio_mttr_90": get_best_mttr(
            subjects=[
                portfolio
                for portfolio in all_portfolios_data_90
                if portfolio.is_valid
            ]
        ),
    }

    worst_portfolio_mttr: Dict[str, Decimal] = {
        "worst_portfolio_mttr": get_worst_mttr(
            subjects=[
                portfolio
                for portfolio in all_portfolios_data
                if portfolio.is_valid
            ],
            oldest_open_age=oldest_open_age,
        ),
        "worst_portfolio_mttr_30": get_worst_mttr(
            subjects=[
                portfolio
                for portfolio in all_portfolios_data_30
                if portfolio.is_valid
            ],
            oldest_open_age=Decimal("30.0"),
        ),
        "worst_portfolio_mttr_90": get_worst_mttr(
            subjects=[
                portfolio
                for portfolio in all_portfolios_data_90
                if portfolio.is_valid
            ],
            oldest_open_age=Decimal("90.0"),
        ),
    }

    _all_groups_data: Dict[str, Tuple[Benchmarking, ...]] = {
        "all_groups_data": all_groups_data,
        "all_groups_data_30": all_groups_data_30,
        "all_groups_data_90": all_groups_data_90,
    }
    _all_organizations_data: Dict[str, Tuple[Benchmarking, ...]] = {
        "all_organizations_data": all_organizations_data,
        "all_organizations_data_30": all_organizations_data_30,
        "all_organizations_data_90": all_organizations_data_90,
    }
    _all_portfolios_data: Dict[str, Tuple[Benchmarking, ...]] = {
        "all_portfolios_data": all_portfolios_data,
        "all_portfolios_data_30": all_portfolios_data_30,
        "all_portfolios_data_90": all_portfolios_data_90,
    }
    header: str = "Categories"

    for days, min_date in zip([None, *list_days], [None, *dates]):
        async for group in iterate_groups():
            document = format_mttr_data(
                data=(
                    (
                        await get_data_one_group(
                            group,
                            loaders,
                            min_date,
                        )
                    ).mttr,
                    best_group_mttr[
                        "best_group_mttr" + get_subject_days(days)
                    ],
                    get_mean_organizations(
                        organizations=get_valid_subjects(
                            all_subjects=_all_groups_data[
                                "all_groups_data" + get_subject_days(days)
                            ],
                            subject=group,
                        )
                    ),
                    worst_group_mttr[
                        "worst_group_mttr" + get_subject_days(days)
                    ],
                ),
                categories=GROUP_CATEGORIES,
            )
            json_dump(
                document=document,
                entity="group",
                subject=group + get_subject_days(days),
                csv_document=format_csv_data(
                    document=document, header=header, alternative=alternative
                ),
            )

        async for org_id, _, org_groups in iterate_organizations_and_groups():
            document = format_mttr_data(
                data=(
                    (
                        await get_data_many_groups_mttr(
                            organization_id=org_id,
                            groups=org_groups,
                            loaders=loaders,
                            get_data_one_group=get_data_one_group,
                            min_date=min_date,
                        )
                    ).mttr,
                    best_mttr["best_mttr" + get_subject_days(days)],
                    get_mean_organizations(
                        organizations=get_valid_subjects(
                            all_subjects=_all_organizations_data[
                                "all_organizations_data"
                                + get_subject_days(days)
                            ],
                            subject=org_id,
                        )
                    ),
                    worst_organazation_mttr[
                        "worst_organazation_mttr" + get_subject_days(days)
                    ],
                ),
                categories=ORGANIZATION_CATEGORIES,
            )
            json_dump(
                document=document,
                entity="organization",
                subject=org_id + get_subject_days(days),
                csv_document=format_csv_data(
                    document=document, header=header, alternative=alternative
                ),
            )

        async for org_id, org_name, _ in iterate_organizations_and_groups():
            for portfolio, pgroup_names in await get_portfolios_groups(
                org_name
            ):
                document = format_mttr_data(
                    data=(
                        (
                            await get_data_many_groups_mttr(
                                organization_id=(
                                    f"{org_id}PORTFOLIO#{portfolio}"
                                ),
                                groups=pgroup_names,
                                loaders=loaders,
                                get_data_one_group=get_data_one_group,
                                min_date=min_date,
                            )
                        ).mttr,
                        best_portfolio_mttr[
                            "best_portfolio_mttr" + get_subject_days(days)
                        ],
                        get_mean_organizations(
                            organizations=get_valid_subjects(
                                all_subjects=_all_portfolios_data[
                                    "all_portfolios_data"
                                    + get_subject_days(days)
                                ],
                                subject=f"{org_id}PORTFOLIO#{portfolio}",
                            )
                        ),
                        worst_portfolio_mttr[
                            "worst_portfolio_mttr" + get_subject_days(days)
                        ],
                    ),
                    categories=PORTFOLIO_CATEGORIES,
                )
                json_dump(
                    document=document,
                    entity="portfolio",
                    subject=f"{org_id}PORTFOLIO#{portfolio}"
                    + get_subject_days(days),
                    csv_document=format_csv_data(
                        document=document,
                        header=header,
                        alternative=alternative,
                    ),
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
    format_csv: Callable[[dict], CsvData],
) -> None:
    loaders = get_new_context()
    async for group in iterate_groups():
        document = format_data(
            await get_data_one_group(group, loaders),
        )
        json_dump(
            document=document,
            entity="group",
            subject=group,
            csv_document=format_csv(document),
        )

    async for org_id, _, org_groups in iterate_organizations_and_groups():
        document = format_data(
            await get_data_many_groups(list(org_groups), loaders),
        )
        json_dump(
            document=document,
            entity="organization",
            subject=org_id,
            csv_document=format_csv(document),
        )

    async for org_id, org_name, _ in iterate_organizations_and_groups():
        for portfolio, groups in await get_portfolios_groups(org_name):
            document = format_data(
                await get_data_many_groups(list(groups), loaders),
            )
            json_dump(
                document=document,
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
                csv_document=format_csv(document),
            )


def format_csv_data(
    *, document: dict, header: str = "Group name", alternative: str = ""
) -> CsvData:
    columns: list[list[str]] = document["data"]["columns"]
    categories: list[str] = document["axis"]["x"]["categories"]
    rows: list[list[str]] = []
    for category, value in zip(categories, tuple(columns[0][1:])):
        try:
            validate_sanitized_csv_input(str(category).rsplit(" - ", 1)[0])
            rows.append([str(category).rsplit(" - ", 1)[0], str(value)])
        except UnsanitizedInputFound:
            rows.append(["", ""])

    return CsvData(
        headers=[header, alternative if alternative else columns[0][0]],
        rows=rows,
    )
