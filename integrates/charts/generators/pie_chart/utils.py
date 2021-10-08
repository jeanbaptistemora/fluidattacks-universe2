from charts.colors import (
    RISK,
)
from charts.utils import (
    get_portfolios_groups,
    iterate_groups,
    iterate_organizations_and_groups,
    json_dump,
)
from decimal import (
    Decimal,
)
from operator import (
    attrgetter,
)
from typing import (
    Any,
    Awaitable,
    Callable,
    Dict,
    List,
    NamedTuple,
    Tuple,
)

PortfoliosGroupsInfo = NamedTuple(
    "PortfoliosGroupsInfo",
    [
        ("group_name", str),
        ("value", Decimal),
    ],
)

MAX_GROUPS_DISPLAYED = 4


def slice_groups(
    groups_data: List[PortfoliosGroupsInfo], total_value: Decimal
) -> List[PortfoliosGroupsInfo]:
    groups_data_sorted = sorted(
        groups_data, key=attrgetter("value"), reverse=True
    )
    groups_data_sliced = groups_data_sorted[:MAX_GROUPS_DISPLAYED]

    if len(groups_data_sorted) > MAX_GROUPS_DISPLAYED:
        return groups_data_sliced + [
            PortfoliosGroupsInfo(
                group_name="others",
                value=total_value
                - sum([group.value for group in groups_data_sliced]),
            )
        ]

    return groups_data_sliced


def format_data(groups_data: List[PortfoliosGroupsInfo]) -> dict:
    return dict(
        data=dict(
            columns=[[group.group_name, group.value] for group in groups_data],
            type="pie",
            colors=dict(
                (group.group_name, color)
                for group, color in zip(groups_data, reversed(RISK))
            ),
        ),
        legend=dict(
            position="right",
        ),
        pie=dict(
            label=dict(
                show=True,
            ),
        ),
    )


async def generate_all(
    *,
    get_data_one_group: Callable[[str], Awaitable[Any]],
    get_data_many_groups: Callable[[Tuple[str, ...]], Awaitable[Any]],
    format_document: Callable[[Any], Dict[str, Any]],
) -> None:
    async for group in iterate_groups():
        json_dump(
            document=format_document(
                await get_data_one_group(group),
            ),
            entity="group",
            subject=group,
        )

    async for org_id, _, org_groups in (iterate_organizations_and_groups()):
        json_dump(
            document=format_document(
                await get_data_many_groups(org_groups),
            ),
            entity="organization",
            subject=org_id,
        )

    async for org_id, org_name, _ in (iterate_organizations_and_groups()):
        for portfolio, groups in await get_portfolios_groups(org_name):
            json_dump(
                document=format_document(
                    await get_data_many_groups(tuple(groups)),
                ),
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
            )
