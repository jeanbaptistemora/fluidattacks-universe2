# Standard library
from collections import Counter
from itertools import groupby
from typing import (
    List,
    Tuple,
    Union,
    cast,
)

# Third party libraries
from aioextensions import (
    collect,
    run,
)
from async_lru import alru_cache

# Local libraries
from charts import utils
from charts.colors import RISK
from dataloaders import get_new_context
from findings.domain import get_finding_open_age


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(group: str) -> Counter:
    context = get_new_context()
    group_findings_loader = context.group_findings
    finding_loader = context.finding

    group_findings_data = await group_findings_loader.load(group.lower())
    finding_ids = [finding['finding_id'] for finding in group_findings_data]
    findings = await finding_loader.load_many(finding_ids)

    return Counter({
        f'{finding_id}/{finding["title"]}': await get_finding_open_age(
            context,
            finding_id
        )
        for finding, finding_id in zip(findings, finding_ids)
    })


async def get_data_many_groups(groups: List[str]) -> Counter:
    groups_data = await collect(map(get_data_one_group, groups))

    return sum(groups_data, Counter())


def format_data(counters: Counter) -> dict:
    data: List[Tuple[str, int]] = [
        (title, open_age)
        for title, open_age in counters.most_common()
        if open_age > 0
    ]

    merged_data: List[List[Union[int, str]]] = []

    for axis, columns in groupby(
        sorted(
            data,
            key=lambda x: utils.get_finding_name([x[0]])
        ),
        lambda x: utils.get_finding_name([x[0]])
    ):
        merged_data.append([axis, max([value for _, value in columns])])

    merged_data = sorted(merged_data, key=lambda x: x[1], reverse=True)[:10]

    return dict(
        data=dict(
            columns=[
                cast(List[Union[int, str]], ['Open Age (days)']) +
                [open_age for _, open_age in merged_data],
            ],
            colors={
                'Open Age (days)': RISK.neutral,
            },
            type='bar',
        ),
        legend=dict(
            position='bottom',
        ),
        axis=dict(
            x=dict(
                categories=[
                    utils.get_finding_name([str(title)])
                    for title, _ in merged_data
                ],
                type='category',
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
    )


async def generate_all() -> None:
    async for org_id, org_name, _ in utils.iterate_organizations_and_groups():
        for portfolio, groups in await utils.get_portfolios_groups(org_name):
            utils.json_dump(
                document=format_data(
                    counters=await get_data_many_groups(groups),
                ),
                entity='portfolio',
                subject=f'{org_id}PORTFOLIO#{portfolio}',
            )


if __name__ == '__main__':
    run(generate_all())
