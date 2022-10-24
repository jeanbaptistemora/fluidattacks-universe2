# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from aioextensions import (
    collect,
    run,
)
from async_lru import (
    alru_cache,
)
from charts.generators.common.colors import (
    RISK,
    TREATMENT,
)
from charts.generators.stacked_bar_chart import (  # type: ignore
    format_csv_data,
)
from charts.generators.stacked_bar_chart.utils import (
    format_stacked_percentages,
    limit_data,
    RemediatedAccepted,
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
) -> RemediatedAccepted:
    indicators: GroupUnreliableIndicators = (
        await loaders.group_unreliable_indicators.load(group_name)
    )
    open_vulnerabilities: int = indicators.open_vulnerabilities or 0
    treatment = indicators.treatment_summary
    if treatment:
        accepted_vulnerabilities: int = (
            treatment.accepted_undefined + treatment.accepted
        )
    else:
        accepted_vulnerabilities = 0
    remaining_open_vulnerabilities: int = (
        open_vulnerabilities - accepted_vulnerabilities
    )
    return RemediatedAccepted(
        group_name=group_name,
        accepted=treatment.accepted if treatment else 0,
        accepted_undefined=treatment.accepted_undefined if treatment else 0,
        remaining_open_vulnerabilities=remaining_open_vulnerabilities
        if remaining_open_vulnerabilities >= 0
        else 0,
        open_vulnerabilities=open_vulnerabilities,
        closed_vulnerabilities=indicators.closed_vulnerabilities or 0,
    )


async def get_data_many_groups(
    loaders: Dataloaders,
    group_names: tuple[str, ...],
) -> list[RemediatedAccepted]:
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


def format_data(
    data: list[RemediatedAccepted],
) -> dict[str, Any]:
    limited_data: list[RemediatedAccepted] = limit_data(data)
    percentage_values = [
        format_stacked_percentages(
            values={
                "Closed": Decimal(group.closed_vulnerabilities),
                "Temporarily accepted": Decimal(group.accepted),
                "Permanently accepted": Decimal(group.accepted_undefined),
                "Open": Decimal(group.remaining_open_vulnerabilities),
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
                ["Temporarily accepted"]
                + [str(group.accepted) for group in limited_data],
                ["Permanently accepted"]
                + [str(group.accepted_undefined) for group in limited_data],
                ["Open"]
                + [
                    str(group.remaining_open_vulnerabilities)
                    for group in limited_data
                ],
            ],
            colors={
                "Closed": RISK.more_passive,
                "Temporarily accepted": TREATMENT.passive,
                "Permanently accepted": TREATMENT.more_passive,
                "Open": RISK.more_agressive,
            },
            labels=dict(
                format=dict(
                    Closed=None,
                ),
            ),
            type="bar",
            groups=[
                [
                    "Closed",
                    "Temporarily accepted",
                    "Permanently accepted",
                    "Open",
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
                categories=[group.group_name for group in limited_data],
                type="category",
                tick=dict(rotate=0, multiline=False),
            ),
            y=dict(
                min=0,
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
            "Closed": [
                percentage_value[0]["Closed"]
                for percentage_value in percentage_values
            ],
            "Temporarily accepted": [
                percentage_value[0]["Temporarily accepted"]
                for percentage_value in percentage_values
            ],
            "Permanently accepted": [
                percentage_value[0]["Permanently accepted"]
                for percentage_value in percentage_values
            ],
            "Open": [
                percentage_value[0]["Open"]
                for percentage_value in percentage_values
            ],
        },
        maxPercentageValues={
            "Closed": [
                percentage_value[1]["Closed"]
                for percentage_value in percentage_values
            ],
            "Temporarily accepted": [
                percentage_value[1]["Temporarily accepted"]
                for percentage_value in percentage_values
            ],
            "Permanently accepted": [
                percentage_value[1]["Permanently accepted"]
                for percentage_value in percentage_values
            ],
            "Open": [
                percentage_value[1]["Open"]
                for percentage_value in percentage_values
            ],
        },
    )


async def generate_all() -> None:
    loaders: Dataloaders = get_new_context()
    header: str = "Group name"
    async for org_id, _, org_group_names in iterate_organizations_and_groups():
        document = format_data(
            data=await get_data_many_groups(loaders, org_group_names),
        )
        json_dump(
            document=document,
            entity="organization",
            subject=org_id,
            csv_document=format_csv_data(document=document, header=header),
        )

    async for org_id, org_name, _ in iterate_organizations_and_groups():
        for portfolio, group_names in await get_portfolios_groups(org_name):
            document = format_data(
                data=await get_data_many_groups(loaders, group_names),
            )
            json_dump(
                document=document,
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
                csv_document=format_csv_data(document=document, header=header),
            )


if __name__ == "__main__":
    run(generate_all())
