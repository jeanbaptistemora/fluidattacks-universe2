from aioextensions import (
    collect,
    run,
)
from async_lru import (
    alru_cache,
)
from charts.colors import (
    RISK,
)
from charts.generators.bar_chart.utils_top_vulnerabilities_by_source import (
    format_max_value,
)
from charts.utils import (
    get_finding_name,
    get_portfolios_groups,
    iterate_organizations_and_groups,
    json_dump,
)
from dataloaders import (
    get_new_context,
)
from db_model.findings.types import (
    Finding,
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
from typing import (
    Any,
    Counter,
    Dict,
    List,
    Tuple,
    Union,
)


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(group: str) -> Counter[str]:
    loaders = get_new_context()
    group_findings: Tuple[Finding, ...] = await loaders.group_findings.load(
        group.lower()
    )
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


async def get_data_many_groups(groups: List[str]) -> Counter[str]:
    groups_data = await collect(map(get_data_one_group, groups), workers=32)

    return sum(groups_data, Counter())


def format_data(counters: Counter[str]) -> Dict[str, Any]:
    data: List[Tuple[str, int]] = [
        (title, open_age)
        for title, open_age in counters.most_common()
        if open_age > 0
    ]
    merged_data: List[List[Union[int, str]]] = []

    for axis, columns in groupby(
        sorted(data, key=lambda x: get_finding_name([x[0]])),
        lambda x: get_finding_name([x[0]]),
    ):
        merged_data.append([axis, max([value for _, value in columns])])

    merged_data = sorted(merged_data, key=lambda x: x[1], reverse=True)[:10]

    return dict(
        data=dict(
            columns=[
                [
                    "Open Age (days)",
                    *[open_age for _, open_age in merged_data],
                ],
            ],
            colors={
                "Open Age (days)": RISK.neutral,
            },
            labels=None,
            type="bar",
        ),
        legend=dict(
            position="bottom",
        ),
        axis=dict(
            x=dict(
                categories=[
                    get_finding_name([str(title)]) for title, _ in merged_data
                ],
                type="category",
                tick=dict(
                    outer=False,
                    rotate=12,
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
            [(key, Decimal(value)) for key, value in merged_data]
        ),
    )


async def generate_all() -> None:
    async for org_id, _, org_groups in iterate_organizations_and_groups():
        json_dump(
            document=format_data(
                counters=await get_data_many_groups(list(org_groups)),
            ),
            entity="organization",
            subject=org_id,
        )

    async for org_id, org_name, _ in iterate_organizations_and_groups():
        for portfolio, groups in await get_portfolios_groups(org_name):
            json_dump(
                document=format_data(
                    counters=await get_data_many_groups(groups),
                ),
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
            )


if __name__ == "__main__":
    run(generate_all())
