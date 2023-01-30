from aioextensions import (
    collect,
    run,
)
from async_lru import (
    alru_cache,
)
from charts.generators.bar_chart import (
    format_csv_data,
)
from charts.generators.bar_chart.mttr_benchmarking_cvssf import (
    _get_historic_verification,
)
from charts.generators.bar_chart.utils import (
    Benchmarking,
    get_valid_subjects,
    get_vulnerability_reattacks,
    GROUP_CATEGORIES,
    ORGANIZATION_CATEGORIES,
    PORTFOLIO_CATEGORIES,
)
from charts.generators.common.colors import (
    EXPOSURE,
)
from charts.generators.common.utils import (
    BAR_RATIO_WIDTH,
    get_max_axis,
)
from charts.generators.stacked_bar_chart.exposed_over_time_cvssf import (
    get_group_document,
)
from charts.generators.stacked_bar_chart.utils import (
    get_current_time_range,
    RiskOverTime,
)
from charts.utils import (
    format_cvssf,
    get_portfolios_groups,
    iterate_groups,
    iterate_organizations_and_groups,
    json_dump,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.vulnerabilities.types import (
    VulnerabilityVerification,
)
from decimal import (
    Decimal,
)
import math
from organizations.domain import (
    get_all_active_group_names,
)
from statistics import (
    mean,
)


def format_cvssf_log(cvssf: Decimal) -> Decimal:
    if cvssf <= Decimal("0.0"):
        return cvssf.quantize(Decimal("0.1"))

    return Decimal(math.log2(cvssf))


def format_max_value(data: tuple[Decimal, ...]) -> Decimal:
    if data:
        return sorted(data, reverse=True)[0]

    return Decimal("1.0")


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(group: str, loaders: Dataloaders) -> Benchmarking:
    group_findings = await loaders.group_findings.load(group.lower())
    vulnerabilities = await loaders.finding_vulnerabilities.load_many_chained(
        [finding.id for finding in group_findings]
    )
    historics_verification: tuple[
        tuple[VulnerabilityVerification, ...], ...
    ] = await collect(
        tuple(
            _get_historic_verification(loaders, vulnerability)
            for vulnerability in vulnerabilities
            if vulnerability.verification
        ),
        workers=4,
    )

    number_of_reattacks = sum(
        get_vulnerability_reattacks(historic_verification=historic)
        for historic in historics_verification
    )

    group_document: RiskOverTime = await get_group_document(group, loaders)
    document = get_current_time_range(tuple([group_document]))[0][0]
    values: list[Decimal] = [
        Decimal(document[name][date]).quantize(Decimal("0.1"))
        for date in tuple(document["date"])[-12:]
        for name in document
        if name != "date"
    ]

    return Benchmarking(
        is_valid=number_of_reattacks > 10,
        subject=group.lower(),
        mttr=values[-1] if len(values) > 0 else Decimal("0.0"),
        number_of_reattacks=number_of_reattacks,
    )


@alru_cache(maxsize=None, typed=True)
async def get_data_many_groups(
    organization_id: str,
    groups: tuple[str, ...],
    loaders: Dataloaders,
) -> Benchmarking:
    groups_data: tuple[Benchmarking, ...] = await collect(
        tuple(get_data_one_group(group, loaders) for group in groups),
        workers=16,
    )

    exposure: Decimal = (
        Decimal(sum(group_data.mttr for group_data in groups_data)).quantize(
            Decimal("0.1")
        )
        if groups_data
        else Decimal("0.0")
    )
    number_of_reattacks = sum(
        group_data.number_of_reattacks for group_data in groups_data
    )

    return Benchmarking(
        is_valid=number_of_reattacks > 100,
        subject=organization_id,
        mttr=exposure,
        number_of_reattacks=number_of_reattacks,
    )


def get_average_entities(*, entities: list[Benchmarking]) -> Decimal:
    return (
        Decimal(mean([subject.mttr for subject in entities])).quantize(
            Decimal("0.1")
        )
        if entities
        else Decimal("0.0")
    )


def get_best_exposure(*, subjects: list[Benchmarking]) -> Decimal:
    return (
        Decimal(min(subject.mttr for subject in subjects)).quantize(
            Decimal("0.1")
        )
        if subjects
        else Decimal("0.0")
    )


def get_worst_exposure(*, subjects: list[Benchmarking]) -> Decimal:

    return (
        Decimal(max(subject.mttr for subject in subjects)).quantize(
            Decimal("0.1")
        )
        if subjects
        else Decimal("0.0")
    )


def format_data(
    all_data: tuple[Decimal, Decimal, Decimal, Decimal],
    categories: list[str],
) -> dict:
    data = tuple(format_cvssf(value) for value in all_data)
    max_value: Decimal = list(
        sorted(
            [abs(value) for value in data],
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
                    "Exposure",
                    *[format_cvssf_log(value) for value in data],
                ]
            ],
            colors={
                "Exposure": EXPOSURE,
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
                    text="CVSSF",
                    position="inner-top",
                ),
                tick=dict(
                    count=5,
                ),
                **(
                    {}
                    if max_axis_value == Decimal("0.0")
                    else dict(max=format_cvssf_log(max_axis_value))
                ),
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
        legend=dict(
            show=False,
        ),
        mttrBenchmarking=True,
        maxValue=format_max_value(data),
        maxValueLog=format_max_value(
            tuple(format_cvssf_log(value) for value in data)
        ),
        originalValues=[
            Decimal(value).quantize(Decimal("0.1")) for value in data
        ],
        grid=dict(
            x=dict(
                show=False,
            ),
            y=dict(
                show=True,
            ),
        ),
        hideYAxisLine=True,
        hideXTickLine=True,
        exposureBenchmarkingCvssf=True,
    )


async def generate() -> None:  # pylint: disable=too-many-locals
    loaders: Dataloaders = get_new_context()
    organizations: list[tuple[str, tuple[str, ...]]] = []
    portfolios: list[tuple[str, tuple[str, ...]]] = []
    group_names: list[str] = list(
        sorted(
            await get_all_active_group_names(loaders),
            reverse=True,
        )
    )

    async for org_id, _, org_groups in iterate_organizations_and_groups():
        organizations.append((org_id, org_groups))

    async for org_id, org_name, _ in iterate_organizations_and_groups():
        for portfolio, p_groups in await get_portfolios_groups(org_name):
            portfolios.append(
                (f"{org_id}PORTFOLIO#{portfolio}", tuple(p_groups))
            )

    all_groups_data: tuple[Benchmarking, ...] = await collect(
        tuple(
            get_data_one_group(
                group_name,
                loaders,
            )
            for group_name in group_names
        ),
        workers=8,
    )

    all_organizations_data: tuple[Benchmarking, ...] = await collect(
        tuple(
            get_data_many_groups(
                organization_id=organization[0],
                groups=organization[1],
                loaders=loaders,
            )
            for organization in organizations
        ),
        workers=8,
    )

    all_portfolios_data: tuple[Benchmarking, ...] = await collect(
        tuple(
            get_data_many_groups(
                organization_id=portfolio[0],
                groups=portfolio[1],
                loaders=loaders,
            )
            for portfolio in portfolios
        ),
        workers=8,
    )

    best_exposure: Decimal = get_best_exposure(
        subjects=[
            organization
            for organization in all_organizations_data
            if organization.is_valid
        ]
    )

    worst_organazation_exposure: Decimal = get_worst_exposure(
        subjects=[
            organization
            for organization in all_organizations_data
            if organization.is_valid
        ],
    )

    best_group_exposure: Decimal = get_best_exposure(
        subjects=[group for group in all_groups_data if group.is_valid]
    )

    worst_group_exposure: Decimal = get_worst_exposure(
        subjects=[group for group in all_groups_data if group.is_valid],
    )

    best_portfolio_exposure: Decimal = get_best_exposure(
        subjects=[
            portfolio
            for portfolio in all_portfolios_data
            if portfolio.is_valid
        ]
    )
    worst_portfolio_exposure: Decimal = get_worst_exposure(
        subjects=[
            portfolio
            for portfolio in all_portfolios_data
            if portfolio.is_valid
        ],
    )

    header: str = "Categories"
    alternative: str = "Exposure"

    async for group in iterate_groups():
        document = format_data(
            all_data=(
                (
                    await get_data_one_group(
                        group,
                        loaders,
                    )
                ).mttr,
                best_group_exposure,
                get_average_entities(
                    entities=get_valid_subjects(
                        all_subjects=all_groups_data,
                    )
                ),
                worst_group_exposure,
            ),
            categories=GROUP_CATEGORIES,
        )
        json_dump(
            document=document,
            entity="group",
            subject=group,
            csv_document=format_csv_data(
                document=document, header=header, alternative=alternative
            ),
        )

    async for org_id, _, org_groups in iterate_organizations_and_groups():
        document = format_data(
            all_data=(
                (
                    await get_data_many_groups(
                        organization_id=org_id,
                        groups=org_groups,
                        loaders=loaders,
                    )
                ).mttr,
                best_exposure,
                get_average_entities(
                    entities=get_valid_subjects(
                        all_subjects=all_organizations_data,
                    )
                ),
                worst_organazation_exposure,
            ),
            categories=ORGANIZATION_CATEGORIES,
        )
        json_dump(
            document=document,
            entity="organization",
            subject=org_id,
            csv_document=format_csv_data(
                document=document, header=header, alternative=alternative
            ),
        )

    async for org_id, org_name, _ in iterate_organizations_and_groups():
        for portfolio, pgroup_names in await get_portfolios_groups(org_name):
            document = format_data(
                all_data=(
                    (
                        await get_data_many_groups(
                            organization_id=f"{org_id}PORTFOLIO#{portfolio}",
                            groups=pgroup_names,
                            loaders=loaders,
                        )
                    ).mttr,
                    best_portfolio_exposure,
                    get_average_entities(
                        entities=get_valid_subjects(
                            all_subjects=all_portfolios_data,
                        )
                    ),
                    worst_portfolio_exposure,
                ),
                categories=PORTFOLIO_CATEGORIES,
            )
            json_dump(
                document=document,
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
                csv_document=format_csv_data(
                    document=document,
                    header=header,
                    alternative=alternative,
                ),
            )


if __name__ == "__main__":
    run(generate())
