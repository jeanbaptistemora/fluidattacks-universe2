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
    limit_data,
    MIN_PERCENTAGE,
    RemediatedStatus,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.groups.types import (
    GroupUnreliableIndicators,
)
from decimal import (
    Decimal,
)
from typing import (
    Any,
)


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(
    loaders: Dataloaders,
    group_name: str,
) -> RemediatedStatus:
    indicators: GroupUnreliableIndicators = (
        await loaders.group_unreliable_indicators.load(group_name)
    )
    return RemediatedStatus(
        group_name=group_name,
        open_vulnerabilities=indicators.open_vulnerabilities or 0,
        closed_vulnerabilities=indicators.closed_vulnerabilities or 0,
    )


async def get_data_many_groups(
    loaders: Dataloaders,
    group_names: list[str],
) -> list[RemediatedStatus]:
    groups_data = await collect(
        [
            get_data_one_group(loaders, group_name)
            for group_name in group_names
        ],
        workers=32,
    )

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
    values: dict[str, Decimal]
) -> tuple[dict[str, str], ...]:
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
    raw_percentages: list[Decimal] = [
        values["Closed"] / total_bar,
        values["Open"] / total_bar,
    ]
    percentages: list[Decimal] = get_percentage(raw_percentages)
    max_percentage_values = dict(
        Closed=str(percentages[0]) if percentages[0] >= MIN_PERCENTAGE else "",
        Open=str(percentages[1]) if percentages[1] >= MIN_PERCENTAGE else "",
    )
    percentage_values = dict(
        Closed=str(percentages[0]),
        Open=str(percentages[1]),
    )

    return (percentage_values, max_percentage_values)


def format_data(
    data: list[RemediatedStatus], size_limit: int = 0
) -> dict[str, Any]:
    limited_data: list[RemediatedStatus] = limit_data(data, size_limit)
    percentage_values = [
        format_percentages(
            {
                "Closed": Decimal(group.closed_vulnerabilities),
                "Open": Decimal(group.open_vulnerabilities),
            }
        )
        for group in limited_data
    ]

    return dict(
        data=dict(
            columns=[
                ["Closed"]
                + [
                    str(group.closed_vulnerabilities) for group in limited_data
                ],
                ["Open"]
                + [str(group.open_vulnerabilities) for group in limited_data],
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
                categories=[group.group_name for group in limited_data],
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
    loaders: Dataloaders = get_new_context()
    async for org_id, _, org_group_names in (
        utils.iterate_organizations_and_groups()
    ):
        utils.json_dump(
            document=format_data(
                data=await get_data_many_groups(
                    loaders, list(org_group_names)
                ),
                size_limit=18,
            ),
            entity="organization",
            subject=org_id,
        )

    async for org_id, org_name, _ in utils.iterate_organizations_and_groups():
        for portfolio, group_names in await utils.get_portfolios_groups(
            org_name
        ):
            utils.json_dump(
                document=format_data(
                    data=await get_data_many_groups(loaders, group_names),
                ),
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
            )


if __name__ == "__main__":
    run(generate_all())
