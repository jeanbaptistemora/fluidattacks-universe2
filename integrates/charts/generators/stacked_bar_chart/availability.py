# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from aioextensions import (
    collect,
    run,
)
from charts.generators.bar_chart.utils import (
    LIMIT,
)
from charts.generators.common.colors import (
    RISK,
)
from charts.generators.pie_chart.availability import (
    EventsAvailability,
    get_data_one_group,
)
from charts.generators.stacked_bar_chart import (  # type: ignore
    format_csv_data,
)
from charts.generators.stacked_bar_chart.utils import (
    get_percentage,
    MIN_PERCENTAGE,
)
from charts.utils import (
    get_portfolios_groups,
    iterate_organizations_and_groups,
    json_dump,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from decimal import (
    Decimal,
)
import operator
from typing import (
    Any,
    Iterable,
)


def get_max_value(counter_values: Iterable[int]) -> int:
    if counter_values and max(list(counter_values)):
        return max(list(counter_values))

    return 1


def format_availability_percentages(
    *, values: dict[str, Decimal]
) -> tuple[dict[str, str], ...]:
    if not values:
        max_percentage_values = {
            "Unavailable": "",
            "Available": "",
        }
        percentage_values = {
            "Unavailable": "0.0",
            "Available": "0.0",
        }

        return (percentage_values, max_percentage_values)

    total_bar: Decimal = values["Unavailable"] + values["Available"]
    total_bar = total_bar if total_bar > Decimal("0.0") else Decimal("0.1")
    raw_percentages: list[Decimal] = [
        values["Unavailable"] / total_bar,
        values["Available"] / total_bar,
    ]
    percentages: list[Decimal] = get_percentage(raw_percentages)
    max_percentage_values = {
        "Unavailable": str(percentages[0])
        if percentages[0] >= MIN_PERCENTAGE
        else "",
        "Available": str(percentages[1])
        if percentages[1] >= MIN_PERCENTAGE
        else "",
    }
    percentage_values = {
        "Unavailable": str(percentages[0]),
        "Available": str(percentages[1]),
    }

    return (percentage_values, max_percentage_values)


def format_data(*, data: tuple[EventsAvailability, ...]) -> dict[str, Any]:
    sorted_data: tuple[EventsAvailability, ...] = tuple(
        sorted(data, key=operator.attrgetter("non_available"), reverse=True)[
            :LIMIT
        ]
    )
    percentage_values = [
        format_availability_percentages(
            values={
                "Unavailable": Decimal(group.non_available),
                "Available": Decimal(group.available),
            }
        )
        for group in sorted_data
    ]

    return dict(
        data=dict(
            columns=[
                ["Unavailable"]
                + [str(group.non_available) for group in sorted_data],
                ["Available"]
                + [str(group.available) for group in sorted_data],
            ],
            colors={
                "Available": RISK.agressive,
                "Unavailable": RISK.passive,
            },
            labels=dict(format={"Unavailable": None}),
            type="bar",
            groups=[
                [
                    "Unavailable",
                    "Available",
                ],
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
            rotated=True,
            x=dict(
                categories=[group.name for group in sorted_data],
                type="category",
                tick=dict(rotate=0, multiline=False),
            ),
            y=dict(
                label=dict(
                    position="outer-top",
                ),
                min=0,
                padding=dict(
                    bottom=0,
                ),
                tick=dict(
                    count=2,
                ),
            ),
        ),
        tooltip=dict(
            format=dict(
                value=None,
            ),
        ),
        percentageValues={
            "Unavailable": [
                percentage_value[0]["Unavailable"]
                for percentage_value in percentage_values
            ],
            "Available": [
                percentage_value[0]["Available"]
                for percentage_value in percentage_values
            ],
        },
        maxPercentageValues={
            "Unavailable": [
                percentage_value[1]["Unavailable"]
                for percentage_value in percentage_values
            ],
            "Available": [
                percentage_value[1]["Available"]
                for percentage_value in percentage_values
            ],
        },
    )


async def get_data_many_groups(
    *, groups: tuple[str, ...], loaders: Dataloaders
) -> tuple[EventsAvailability, ...]:
    return await collect(
        tuple(
            get_data_one_group(group_name=group, loaders=loaders)
            for group in groups
        ),
        workers=32,
    )


async def generate_all() -> None:
    header: str = "Group name"
    loaders: Dataloaders = get_new_context()
    async for org_id, _, org_groups in iterate_organizations_and_groups():
        document = format_data(
            data=await get_data_many_groups(
                groups=org_groups, loaders=loaders
            ),
        )
        json_dump(
            document=document,
            entity="organization",
            subject=org_id,
            csv_document=format_csv_data(document=document, header=header),
        )

    async for org_id, org_name, _ in iterate_organizations_and_groups():
        for portfolio, groups in await get_portfolios_groups(org_name):
            document = format_data(
                data=await get_data_many_groups(
                    groups=tuple(groups), loaders=loaders
                ),
            )
            json_dump(
                document=document,
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
                csv_document=format_csv_data(document=document, header=header),
            )


if __name__ == "__main__":
    run(generate_all())
