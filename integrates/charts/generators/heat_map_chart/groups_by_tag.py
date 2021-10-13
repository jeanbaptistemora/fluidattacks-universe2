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
    Counter,
    List,
    NamedTuple,
    Set,
    Tuple,
)

GroupsTags = NamedTuple(
    "GroupsTags",
    [
        ("counter", Counter[str]),
        ("counter_group", Counter[str]),
        ("groups", List[str]),
        ("tags", Set[str]),
    ],
)


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(group: str) -> GroupsTags:
    context = get_new_context()
    group_findings_loader = context.group_findings
    group_findings: Tuple[Finding, ...] = await group_findings_loader.load(
        group.lower()
    )
    finding_ids = [finding.id for finding in group_findings]

    vulnerabilities = await context.finding_vulns_nzr.load_many_chained(
        finding_ids
    )

    tags: List[str] = list(
        filter(
            None,
            chain.from_iterable(
                map(lambda x: x["tag"].split(", "), vulnerabilities)
            ),
        )
    )

    return GroupsTags(
        counter=Counter(tags),
        counter_group=Counter([f"{group.lower()}/{tag}" for tag in tags]),
        groups=[group] if tags else [],
        tags=set(tags),
    )


async def get_data_many_groups(groups: List[str]) -> GroupsTags:
    groups_data = await collect(map(get_data_one_group, groups))
    all_tags = [group_data.tags for group_data in groups_data]

    return GroupsTags(
        counter=sum(
            [group_data.counter for group_data in groups_data], Counter()
        ),
        counter_group=sum(
            [group_data.counter_group for group_data in groups_data], Counter()
        ),
        groups=[
            group.lower()
            for group, group_data in zip(groups, groups_data)
            if group_data.groups
        ],
        tags=set.union(*all_tags) if all_tags else set(),
    )


def format_data(data: GroupsTags) -> dict:
    max_value: List[Tuple[str, int]] = data.counter_group.most_common(1)
    tags: Set[str] = {tag for tag, _ in data.counter.most_common()[:10]}
    groups: Set[str] = {
        group
        for group in data.groups
        for tag in tags
        if data.counter_group[f"{group}/{tag}"] > 0
    }

    return dict(
        x=groups,
        grid_values=[
            {
                "value": data.counter_group[f"{group}/{tag}"],
                "x": group,
                "y": tag,
            }
            for group in groups
            for tag in tags
        ],
        y=tags,
        max_value=max_value[0][1] if max_value else 1,
        tick_rotate=utils.TICK_ROTATION,
    )


async def generate_all() -> None:
    async for org_id, _, org_groups in (
        utils.iterate_organizations_and_groups()
    ):
        utils.json_dump(
            document=format_data(
                data=await get_data_many_groups(list(org_groups)),
            ),
            entity="organization",
            subject=org_id,
        )

    async for org_id, org_name, _ in utils.iterate_organizations_and_groups():
        for portfolio, groups in await utils.get_portfolios_groups(org_name):
            utils.json_dump(
                document=format_data(data=await get_data_many_groups(groups)),
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
            )


if __name__ == "__main__":
    run(generate_all())
