from aioextensions import (
    collect,
    run,
)
from async_lru import (
    alru_cache,
)
from charts.generators.bar_chart.utils import (
    format_data_csv,
    LIMIT,
)
from charts.generators.bar_chart.utils_top_vulnerabilities_by_source import (
    format_max_value,
)
from charts.generators.common.colors import (
    OTHER_COUNT,
)
from charts.generators.common.utils import (
    get_finding_name,
)
from charts.utils import (
    CsvData,
    get_portfolios_groups,
    iterate_organizations_and_groups,
    json_dump,
)
from collections import (
    Counter,
)
from dataloaders import (
    get_new_context,
)
from decimal import (
    Decimal,
)
from findings.domain import (
    get_finding_open_age,
)
from itertools import (
    groupby,
)


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(group: str) -> Counter[str]:
    loaders = get_new_context()
    group_findings = await loaders.group_findings.load(group.lower())
    findings_open_age = await collect(
        tuple(
            get_finding_open_age(loaders, finding.id)
            for finding in group_findings
        ),
        workers=32,
    )
    counter: Counter[str] = Counter(
        {
            f"{finding.id}/{finding.title}": open_age
            for finding, open_age in zip(group_findings, findings_open_age)
        }
    )

    return counter


async def get_data_many_groups(groups: tuple[str, ...]) -> Counter[str]:
    groups_data = await collect(map(get_data_one_group, groups), workers=32)

    return sum(groups_data, Counter())


def format_data(counters: Counter[str]) -> tuple[dict, CsvData]:
    data: list[tuple[str, int]] = [
        (title, open_age)
        for title, open_age in counters.most_common()
        if open_age > 0
    ]
    merged_data: list[list[int | str]] = []

    for axis, columns in groupby(
        sorted(data, key=lambda x: get_finding_name([x[0]])),
        lambda x: get_finding_name([x[0]]),
    ):
        merged_data.append([axis, max(value for _, value in columns)])

    merged_data = sorted(merged_data, key=lambda x: x[1], reverse=True)
    limited_merged_data = merged_data[:LIMIT]

    json_data: dict = dict(
        data=dict(
            columns=[
                [
                    "Open Age (days)",
                    *[open_age for _, open_age in limited_merged_data],
                ],
            ],
            colors={
                "Open Age (days)": OTHER_COUNT,
            },
            labels=None,
            type="bar",
        ),
        legend=dict(
            show=False,
        ),
        padding=dict(
            bottom=0,
        ),
        axis=dict(
            rotated=True,
            x=dict(
                categories=[
                    get_finding_name([str(title)])
                    for title, _ in limited_merged_data
                ],
                type="category",
                tick=dict(
                    multiline=False,
                    outer=False,
                    rotate=0,
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
        maxValue=format_max_value(
            [(str(key), Decimal(value)) for key, value in limited_merged_data]
        ),
        exposureTrendsByCategories=True,
        keepToltipColor=True,
    )

    csv_data = format_data_csv(
        header_value=str(json_data["data"]["columns"][0][0]),
        values=[Decimal(value) for _, value in merged_data],
        categories=[str(group) for group, _ in merged_data],
        header_title="Type",
    )

    return (json_data, csv_data)


async def generate_all() -> None:
    async for org_id, _, org_groups in iterate_organizations_and_groups():
        json_document, csv_document = format_data(
            counters=await get_data_many_groups(org_groups),
        )
        json_dump(
            document=json_document,
            entity="organization",
            subject=org_id,
            csv_document=csv_document,
        )

    async for org_id, org_name, _ in iterate_organizations_and_groups():
        for portfolio, groups in await get_portfolios_groups(org_name):
            json_document, csv_document = format_data(
                counters=await get_data_many_groups(groups),
            )
            json_dump(
                document=json_document,
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
                csv_document=csv_document,
            )


if __name__ == "__main__":
    run(generate_all())
