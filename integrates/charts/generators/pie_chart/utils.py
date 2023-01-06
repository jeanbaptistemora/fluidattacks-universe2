from charts.generators.common.colors import (
    RISK,
)
from charts.generators.pie_chart.common import (
    format_csv_data,
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
    NamedTuple,
)


class PortfoliosGroupsInfo(NamedTuple):
    group_name: str
    value: Decimal


MAX_GROUPS_DISPLAYED = 4


def slice_groups(
    groups_data: tuple[PortfoliosGroupsInfo, ...], total_value: Decimal
) -> list[PortfoliosGroupsInfo]:
    groups_data_sorted = sorted(
        groups_data, key=attrgetter("value"), reverse=True
    )
    groups_data_sliced = groups_data_sorted[:MAX_GROUPS_DISPLAYED]

    if len(groups_data_sorted) > MAX_GROUPS_DISPLAYED:
        return groups_data_sliced + [
            PortfoliosGroupsInfo(
                group_name="others",
                value=total_value
                - sum(group.value for group in groups_data_sliced),
            )
        ]

    return groups_data_sliced


def format_data(groups_data: list[PortfoliosGroupsInfo]) -> dict:
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
    get_data_many_groups: Callable[[tuple[str, ...]], Awaitable[Any]],
    format_document: Callable[[Any], dict[str, Any]],
    header: list[str],
) -> None:
    async for group in iterate_groups():
        document = format_document(
            await get_data_one_group(group),
        )
        json_dump(
            document=document,
            entity="group",
            subject=group,
            csv_document=format_csv_data(document=document, header=header),
        )

    async for org_id, _, org_groups in iterate_organizations_and_groups():
        document = format_document(
            await get_data_many_groups(org_groups),
        )
        json_dump(
            document=document,
            entity="organization",
            subject=org_id,
            csv_document=format_csv_data(document=document, header=header),
        )

    async for org_id, org_name, _ in iterate_organizations_and_groups():
        for portfolio, groups in await get_portfolios_groups(org_name):
            document = format_document(
                await get_data_many_groups(tuple(groups)),
            )
            json_dump(
                document=document,
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
                csv_document=format_csv_data(document=document, header=header),
            )
