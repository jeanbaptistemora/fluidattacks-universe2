from aioextensions import (
    collect,
    run,
)
from async_lru import (
    alru_cache,
)
from charts.generators.bar_chart import (  # type: ignore
    format_csv_data,
)
from charts.generators.bar_chart.utils_top_vulnerabilities_by_source import (
    format_max_value,
)
from charts.generators.common.colors import (
    RISK,
)
from charts.generators.common.utils import (
    CRITERIA_VULNERABILITIES,
    format_cvssf_log_adjusted,
    get_max_axis,
)
from charts.generators.gauge.severity import (
    MaxSeverity,
)
from charts.generators.text_box.utils_vulnerabilities_remediation import (
    had_state_by_then,
)
from charts.utils import (
    format_cvssf,
    get_cvssf,
    get_portfolios_groups,
    iterate_groups,
    iterate_organizations_and_groups,
    json_dump,
)
from contextlib import (
    suppress,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from decimal import (
    Decimal,
)
from findings.domain.core import (
    get_severity_score,
)
from newutils.datetime import (
    get_now_minus_delta,
)
from ruamel import (
    yaml,
)
from typing import (
    Counter,
    NamedTuple,
)


class GroupInformation(NamedTuple):
    categories: dict[str, str]
    cvssf: dict[str, Decimal]
    finding_vulnerabilities: tuple[tuple[Vulnerability, ...], ...]
    findings: tuple[Finding, ...]


def get_categories() -> dict[str, str]:
    categories: dict[str, str] = {}
    with open(CRITERIA_VULNERABILITIES, encoding="utf-8") as handle:
        for code, data in yaml.safe_load(handle).items():
            categories[code] = data["category"]

    return categories


CATEGORIES: dict[str, str] = get_categories()


def get_category(*, finding_title: str, categories: dict[str, str]) -> str:
    with suppress(KeyError):
        return categories[finding_title.split(".")[0]]

    return ""


@alru_cache(maxsize=None, typed=True)
async def get_data_vulnerabilities(
    *,
    group: str,
    loaders: Dataloaders,
) -> GroupInformation:
    findings: tuple[Finding, ...] = await loaders.group_findings.load(group)
    finding_cvssf: dict[str, Decimal] = {
        finding.id: get_cvssf(get_severity_score(finding.severity))
        for finding in findings
    }
    finding_category: dict[str, str] = {
        finding.id: get_category(
            finding_title=finding.title, categories=CATEGORIES
        )
        for finding in findings
    }

    vulnerabilities: tuple[
        tuple[Vulnerability, ...], ...
    ] = await loaders.finding_vulnerabilities_released_nzr.load_many(
        [finding.id for finding in findings]
    )

    return GroupInformation(
        categories=finding_category,
        cvssf=finding_cvssf,
        finding_vulnerabilities=vulnerabilities,
        findings=findings,
    )


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(
    *,
    group: str,
    loaders: Dataloaders,
    days: int = 30,
) -> Counter[str]:
    last_day: datetime = get_now_minus_delta(days=days)
    data: GroupInformation = await get_data_vulnerabilities(
        group=group,
        loaders=loaders,
    )

    vulnerabilities_by_categories = [
        {
            f"{data.categories[finding.id]}/open": had_state_by_then(
                last_day=last_day,
                state=VulnerabilityStateStatus.OPEN,
                vulnerabilities=vulnerabilities,
                findings_cvssf=data.cvssf,
                sprint=True,
            ).quantize(Decimal("0.001")),
            f"{data.categories[finding.id]}/closed": had_state_by_then(
                last_day=last_day,
                state=VulnerabilityStateStatus.CLOSED,
                vulnerabilities=vulnerabilities,
                findings_cvssf=data.cvssf,
                sprint=True,
            ).quantize(Decimal("0.001")),
        }
        for finding, vulnerabilities in zip(
            data.findings, data.finding_vulnerabilities
        )
    ]

    return sum(
        [Counter(source) for source in vulnerabilities_by_categories],
        Counter(),
    )


async def get_data_many_groups(
    *,
    groups: tuple[str, ...],
    loaders: Dataloaders,
    days: int,
) -> Counter[str]:
    groups_data: tuple[Counter[str], ...] = await collect(
        tuple(
            get_data_one_group(group=group, loaders=loaders, days=days)
            for group in groups
        ),
        workers=32,
    )

    return sum(groups_data, Counter())


def sorter(item: MaxSeverity) -> tuple[Decimal, int]:
    return (
        format_cvssf(item.value),
        -ord(item.name[0]) if item.name else 0,
    )


def format_data(data: Counter[str], categories: list[str]) -> dict:
    categories_trend: list[MaxSeverity] = [
        MaxSeverity(
            name=category,
            value=Decimal(
                data[f"{category}/open"] - data[f"{category}/closed"]
            ),
        )
        for category in categories
    ]
    categories_trend = [
        MaxSeverity(name=category.name, value=format_cvssf(category.value))
        for category in categories_trend
    ]
    categories_trend = sorted(categories_trend, key=sorter, reverse=True)
    max_value: Decimal = list(
        sorted(
            [
                abs(format_cvssf(category.value))
                for category in categories_trend
            ],
            reverse=True,
        )
    )[0]
    max_axis_value: Decimal = (
        get_max_axis(value=max_value)
        if max_value > Decimal("0.0")
        else Decimal("0.0")
    )
    min_axis_value: Decimal = max_axis_value * Decimal("-1.0")

    return dict(
        data=dict(
            columns=[
                ["Exposure"]
                + [
                    format_cvssf_log_adjusted(category.value)
                    for category in categories_trend
                ],
            ],
            color=None,
            colors={
                "Exposure": RISK.more_agressive,
            },
            labels=None,
            type="bar",
        ),
        legend=dict(
            show=False,
        ),
        grid=dict(
            x=dict(
                show=False,
            ),
            y=dict(
                show=True,
            ),
        ),
        axis=dict(
            rotated=True,
            x=dict(
                categories=[category.name for category in categories_trend],
                type="category",
                tick=dict(
                    rotate=0,
                    multiline=False,
                ),
            ),
            y=dict(
                label=dict(
                    text="CVSSF",
                    position="outer-top",
                ),
                tick=dict(
                    count=7,
                ),
                min=format_cvssf_log_adjusted(min_axis_value),
                max=format_cvssf_log_adjusted(max_axis_value),
            ),
        ),
        maxValueLogAdjusted=format_max_value(
            [
                (category.name, format_cvssf_log_adjusted(abs(category.value)))
                for category in categories_trend
            ]
        ),
        originalValues=[
            format_cvssf(category.value) for category in categories_trend
        ],
        exposureTrendsByCategories=True,
    )


def get_subject_days(days: int) -> str:
    if days == 30:
        return ""
    return f"_{days}"


async def generate_all() -> None:
    loaders: Dataloaders = get_new_context()
    unique_categories: list[str] = list(sorted(set(CATEGORIES.values())))
    category: str = "Categories"
    list_days: list[int] = [30, 60, 90, 180]
    for days in list_days:
        async for group in iterate_groups():
            document = format_data(
                data=await get_data_one_group(
                    group=group, loaders=loaders, days=days
                ),
                categories=unique_categories,
            )
            json_dump(
                document=document,
                entity="group",
                subject=group + get_subject_days(days),
                csv_document=format_csv_data(
                    document=document, header=category
                ),
            )

        async for org_id, _, org_groups in iterate_organizations_and_groups():
            document = format_data(
                data=await get_data_many_groups(
                    groups=org_groups,
                    loaders=loaders,
                    days=days,
                ),
                categories=unique_categories,
            )
            json_dump(
                document=document,
                entity="organization",
                subject=org_id + get_subject_days(days),
                csv_document=format_csv_data(
                    document=document, header=category
                ),
            )

        async for org_id, org_name, _ in iterate_organizations_and_groups():
            for portfolio, groups in await get_portfolios_groups(org_name):
                document = format_data(
                    data=await get_data_many_groups(
                        groups=tuple(groups),
                        loaders=loaders,
                        days=days,
                    ),
                    categories=unique_categories,
                )
                json_dump(
                    document=document,
                    entity="portfolio",
                    subject=f"{org_id}PORTFOLIO#{portfolio}"
                    + get_subject_days(days),
                    csv_document=format_csv_data(
                        document=document, header=category
                    ),
                )


if __name__ == "__main__":
    run(generate_all())
