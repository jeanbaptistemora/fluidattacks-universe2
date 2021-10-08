from aioextensions import (
    collect,
    run,
)
from async_lru import (
    alru_cache,
)
from charts import (
    utils,
)
from charts.colors import (
    RISK,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.findings.types import (
    Finding,
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
async def get_data_one_group(group: str, loaders: Dataloaders) -> Counter[str]:
    group_findings_new: Tuple[
        Finding, ...
    ] = await loaders.group_findings_new.load(group.lower())
    finding_ids = [finding.id for finding in group_findings_new]
    finding_vulns = await loaders.finding_vulns_nzr.load_many(finding_ids)
    counter = Counter(
        [
            f"{finding.id}/{finding.title}"
            for finding, vulnerabilities in zip(
                group_findings_new, finding_vulns
            )
            for vulnerability in vulnerabilities
            if vulnerability["current_state"] == "open"
        ]
    )

    return counter


async def get_data_many_groups(
    groups: List[str], loaders: Dataloaders
) -> Counter[str]:
    groups_data = await collect(
        [get_data_one_group(group, loaders) for group in groups]
    )

    return sum(groups_data, Counter())


def format_data(counters: Counter[str]) -> Dict[str, Any]:
    data: List[Tuple[str, int]] = counters.most_common()
    merged_data: List[List[Union[int, str]]] = []
    for axis, columns in groupby(
        sorted(data, key=lambda x: utils.get_finding_name([x[0]])),
        key=lambda x: utils.get_finding_name([x[0]]),
    ):
        merged_data.append([axis, sum([value for _, value in columns])])

    merged_data = sorted(merged_data, key=lambda x: x[1], reverse=True)[:10]

    return dict(
        data=dict(
            columns=[
                [
                    "# Open Vulnerabilities",
                    *[value for _, value in merged_data],
                ],
            ],
            colors={
                "# Open Vulnerabilities": RISK.neutral,
            },
            type="bar",
        ),
        legend=dict(
            position="bottom",
        ),
        axis=dict(
            x=dict(
                categories=[
                    utils.get_finding_name([str(key)])
                    for key, _ in merged_data
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
    )


async def generate_all() -> None:
    loaders = get_new_context()
    async for group in utils.iterate_groups():
        utils.json_dump(
            document=format_data(
                counters=await get_data_one_group(group, loaders)
            ),
            entity="group",
            subject=group,
        )

    async for org_id, _, org_groups in (
        utils.iterate_organizations_and_groups()
    ):
        utils.json_dump(
            document=format_data(
                counters=await get_data_many_groups(list(org_groups), loaders),
            ),
            entity="organization",
            subject=org_id,
        )

    async for org_id, org_name, _ in utils.iterate_organizations_and_groups():
        for portfolio, groups in await utils.get_portfolios_groups(org_name):
            utils.json_dump(
                document=format_data(
                    counters=await get_data_many_groups(list(groups), loaders),
                ),
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
            )


if __name__ == "__main__":
    run(generate_all())
