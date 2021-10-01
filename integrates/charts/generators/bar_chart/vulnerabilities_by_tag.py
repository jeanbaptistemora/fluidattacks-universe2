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
from collections import (
    Counter,
)
from context import (
    FI_API_STATUS,
)
from dataloaders import (
    get_new_context,
)
from db_model.findings.types import (
    Finding,
)
from itertools import (
    chain,
)
from typing import (
    cast,
    List,
    Tuple,
    Union,
)


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(group: str) -> Counter:
    context = get_new_context()
    if FI_API_STATUS == "migration":
        group_findings_new_loader = context.group_findings_new
        group_findings_new: Tuple[
            Finding, ...
        ] = await group_findings_new_loader.load(group.lower())
        finding_ids = [finding.id for finding in group_findings_new]
    else:
        group_findings_loader = context.group_findings
        group_findings_data = await group_findings_loader.load(group.lower())
        finding_ids = [
            finding["finding_id"] for finding in group_findings_data
        ]

    vulnerabilities = await context.finding_vulns_nzr.load_many_chained(
        finding_ids
    )

    return Counter(
        filter(
            None,
            chain.from_iterable(
                map(lambda x: x["tag"].split(", "), vulnerabilities)
            ),
        )
    )


async def get_data_many_groups(groups: List[str]) -> Counter:
    groups_data = await collect(map(get_data_one_group, groups))

    return sum(groups_data, Counter())


def format_data(counters: Counter) -> dict:
    data = counters.most_common()[:12]

    return dict(
        data=dict(
            columns=[
                cast(List[Union[int, str]], ["Tag"])
                + [value for _, value in data],
            ],
            colors={
                "Tag": RISK.neutral,
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
                    rotate=utils.TICK_ROTATION,
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


async def generate_all() -> None:
    async for group in utils.iterate_groups():
        utils.json_dump(
            document=format_data(
                counters=await get_data_one_group(group),
            ),
            entity="group",
            subject=group,
        )

    async for org_id, _, org_groups in (
        utils.iterate_organizations_and_groups()
    ):
        utils.json_dump(
            document=format_data(
                counters=await get_data_many_groups(list(org_groups)),
            ),
            entity="organization",
            subject=org_id,
        )

    async for org_id, org_name, _ in utils.iterate_organizations_and_groups():
        for portfolio, groups in await utils.get_portfolios_groups(org_name):
            utils.json_dump(
                document=format_data(
                    counters=await get_data_many_groups(groups),
                ),
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
            )


if __name__ == "__main__":
    run(generate_all())
