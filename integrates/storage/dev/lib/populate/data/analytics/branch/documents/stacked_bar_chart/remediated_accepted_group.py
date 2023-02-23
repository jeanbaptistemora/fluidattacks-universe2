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
from charts.generators.stacked_bar_chart.utils import (
    format_data_csv,
    format_stacked_percentages,
    limit_data,
    RemediatedAccepted,
)
from charts.utils import (
    CsvData,
    get_portfolios_groups,
    iterate_organizations_and_groups,
    json_dump,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.groups.types import (
    GroupTreatmentSummary,
    GroupUnreliableIndicators,
)
from decimal import (
    Decimal,
)
from typing import (
    Optional,
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
    treatment: Optional[GroupTreatmentSummary] = indicators.treatment_summary
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
            x.open_vulnerabilities
            / (x.closed_vulnerabilities + x.open_vulnerabilities)
            if (x.closed_vulnerabilities + x.open_vulnerabilities) > 0
            else 0
        ),
        reverse=True,
    )


def format_data(
    data: list[RemediatedAccepted],
) -> tuple[dict, CsvData]:
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

    json_data = dict(
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

    csv_data = format_data_csv(
        columns=[
            "Closed",
            "Temporarily accepted",
            "Permanently accepted",
            "Open",
        ],
        values=[
            [Decimal(group.closed_vulnerabilities) for group in data],
            [Decimal(group.accepted) for group in data],
            [Decimal(group.accepted_undefined) for group in data],
            [Decimal(group.remaining_open_vulnerabilities) for group in data],
        ],
        categories=[group.group_name for group in data],
        header="Group name",
    )

    return (json_data, csv_data)


async def generate_all() -> None:
    loaders: Dataloaders = get_new_context()
    async for org_id, _, org_group_names in iterate_organizations_and_groups():
        json_document, csv_document = format_data(
            data=await get_data_many_groups(loaders, org_group_names),
        )
        json_dump(
            document=json_document,
            entity="organization",
            subject=org_id,
            csv_document=csv_document,
        )

    async for org_id, org_name, _ in iterate_organizations_and_groups():
        for portfolio, group_names in await get_portfolios_groups(org_name):
            json_document, csv_document = format_data(
                data=await get_data_many_groups(loaders, group_names),
            )
            json_dump(
                document=json_document,
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
                csv_document=csv_document,
            )


if __name__ == "__main__":
    run(generate_all())
