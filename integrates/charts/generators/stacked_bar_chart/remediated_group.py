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
from charts.generators.stacked_bar_chart.utils import (
    get_percentage,
)
from decimal import (
    Decimal,
)
from groups import (
    domain as groups_domain,
)
from typing import (
    Any,
    Dict,
    List,
    NamedTuple,
    Tuple,
)

Status = NamedTuple(
    "Status",
    [
        ("group_name", str),
        ("closed_vulnerabilities", int),
        ("open_vulnerabilities", int),
    ],
)


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(group: str) -> Status:
    item = await groups_domain.get_attributes(
        group,
        [
            "open_vulnerabilities",
            "closed_vulnerabilities",
        ],
    )

    return Status(
        group_name=group.lower(),
        open_vulnerabilities=item.get("open_vulnerabilities", 0),
        closed_vulnerabilities=item.get("closed_vulnerabilities", 0),
    )


async def get_data_many_groups(groups: List[str]) -> List[Status]:
    groups_data = await collect(map(get_data_one_group, groups))

    return sorted(
        groups_data,
        key=lambda x: (
            x.closed_vulnerabilities
            / (x.closed_vulnerabilities + x.open_vulnerabilities)
            if (x.closed_vulnerabilities + x.open_vulnerabilities) > 0
            else 0
        ),
    )


def format_percentages(
    values: Dict[str, Decimal]
) -> Tuple[Dict[str, str], ...]:
    if not values:
        max_percentage_values = dict(
            Closed="",
            Open="",
        )
        percentage_values = dict(
            Closed="0.0",
            Open="0.0",
        )

        return (percentage_values, max_percentage_values)

    total_bar: Decimal = values["Closed"] + values["Open"]
    total_bar = total_bar if total_bar > Decimal("0.0") else Decimal("0.1")
    raw_percentages: List[Decimal] = [
        values["Closed"] / total_bar,
        values["Open"] / total_bar,
    ]
    percentages: List[Decimal] = get_percentage(raw_percentages)
    max_percentages = max(percentages) if max(percentages) else ""
    is_first_value_max: bool = percentages[0] == max_percentages
    is_second_value_max: bool = percentages[1] == max_percentages
    max_percentage_values = dict(
        Closed=str(percentages[0]) if is_first_value_max else "",
        Open=str(percentages[1])
        if is_second_value_max and not is_first_value_max
        else "",
    )
    percentage_values = dict(
        Closed=str(percentages[0]),
        Open=str(percentages[1]),
    )

    return (percentage_values, max_percentage_values)


def format_data(data: List[Status]) -> Dict[str, Any]:
    percentage_values = [
        format_percentages(
            {
                "Closed": Decimal(group.closed_vulnerabilities),
                "Open": Decimal(group.open_vulnerabilities),
            }
        )
        for group in data
    ]

    return dict(
        data=dict(
            columns=[
                ["Closed"]
                + [str(group.closed_vulnerabilities) for group in data],
                ["Open"] + [str(group.open_vulnerabilities) for group in data],
            ],
            colors={
                "Closed": RISK.more_passive,
                "Open": RISK.more_agressive,
            },
            labels=dict(
                format=dict(
                    Accepted=None,
                ),
            ),
            type="bar",
            groups=[
                ["Closed", "Open"],
            ],
            order=None,
            stack=dict(
                normalize=True,
            ),
        ),
        legend=dict(
            position="bottom",
        ),
        axis=dict(
            x=dict(
                categories=[group.group_name for group in data],
                type="category",
                tick=dict(rotate=utils.TICK_ROTATION, multiline=False),
            ),
        ),
        tooltip=dict(
            format=dict(
                value=None,
            ),
        ),
        percentageValues=dict(
            Closed=[
                percentage_value[0]["Closed"]
                for percentage_value in percentage_values
            ],
            Open=[
                percentage_value[0]["Open"]
                for percentage_value in percentage_values
            ],
        ),
        maxPercentageValues=dict(
            Closed=[
                percentage_value[1]["Closed"]
                for percentage_value in percentage_values
            ],
            Open=[
                percentage_value[1]["Open"]
                for percentage_value in percentage_values
            ],
        ),
    )


async def generate_all() -> None:
    async for org_id, org_name, _ in (
        utils.iterate_organizations_and_groups()
    ):
        for portfolio, groups in await utils.get_portfolios_groups(org_name):
            utils.json_dump(
                document=format_data(
                    data=await get_data_many_groups(groups),
                ),
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
            )


if __name__ == "__main__":
    run(generate_all())
