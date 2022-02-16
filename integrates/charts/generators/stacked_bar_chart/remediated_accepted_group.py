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
    TREATMENT,
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

Treatment = NamedTuple(
    "Treatment",
    [
        ("accepted", int),
        ("accepted_undefined", int),
        ("group_name", str),
        ("closed_vulnerabilities", int),
        ("open_vulnerabilities", int),
        ("remaining_open_vulnerabilities", int),
    ],
)


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(group: str) -> Treatment:
    item = await groups_domain.get_attributes(
        group,
        [
            "open_vulnerabilities",
            "closed_vulnerabilities",
            "total_treatment",
        ],
    )
    treatment = item.get("total_treatment", {})
    open_vulnerabilities: int = item.get("open_vulnerabilities", 0)
    accepted_vulnerabilities: int = treatment.get(
        "acceptedUndefined", 0
    ) + treatment.get("accepted", 0)
    remaining_open_vulnerabilities: int = (
        open_vulnerabilities - accepted_vulnerabilities
    )

    return Treatment(
        group_name=group.lower(),
        accepted=treatment.get("accepted", 0),
        accepted_undefined=treatment.get("acceptedUndefined", 0),
        remaining_open_vulnerabilities=remaining_open_vulnerabilities
        if remaining_open_vulnerabilities >= 0
        else 0,
        open_vulnerabilities=open_vulnerabilities,
        closed_vulnerabilities=item.get("closed_vulnerabilities", 0),
    )


async def get_data_many_groups(groups: List[str]) -> List[Treatment]:
    groups_data = await collect(map(get_data_one_group, groups), workers=32)

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
        max_percentage_values = {
            "Closed": "",
            "Temporarily Accepted": "",
            "Permanently accepted": "",
            "Open": "",
        }
        percentage_values = {
            "Closed": "0.0",
            "Temporarily Accepted": "0.0",
            "Permanently accepted": "0.0",
            "Open": "0.0",
        }

        return (percentage_values, max_percentage_values)

    total_bar: Decimal = (
        values["Closed"]
        + values["Temporarily Accepted"]
        + values["Permanently accepted"]
        + values["Open"]
    )
    total_bar = total_bar if total_bar > Decimal("0.0") else Decimal("0.1")
    raw_percentages: List[Decimal] = [
        values["Closed"] / total_bar,
        values["Temporarily Accepted"] / total_bar,
        values["Permanently accepted"] / total_bar,
        values["Open"] / total_bar,
    ]
    percentages: List[Decimal] = get_percentage(raw_percentages)
    max_percentages = max(percentages) if max(percentages) else ""
    is_first_value_max: bool = percentages[0] == max_percentages
    is_second_value_max: bool = percentages[1] == max_percentages
    is_third_value_max: bool = percentages[2] == max_percentages
    is_fourth_value_max: bool = percentages[3] == max_percentages
    max_percentage_values = {
        "Closed": str(percentages[0]) if is_first_value_max else "",
        "Temporarily Accepted": str(percentages[1])
        if is_second_value_max and not is_first_value_max
        else "",
        "Permanently accepted": str(percentages[2])
        if is_third_value_max
        and not (is_first_value_max or is_second_value_max)
        else "",
        "Open": str(percentages[3])
        if is_fourth_value_max
        and not (
            is_first_value_max or is_second_value_max or is_third_value_max
        )
        else "",
    }
    percentage_values = {
        "Closed": str(percentages[0]),
        "Temporarily Accepted": str(percentages[1]),
        "Permanently accepted": str(percentages[2]),
        "Open": str(percentages[3]),
    }

    return (percentage_values, max_percentage_values)


def format_data(data: List[Treatment], limit: int = 0) -> Dict[str, Any]:
    limited_data = list(reversed(data))[:limit] if limit else list(data)
    percentage_values = [
        format_percentages(
            {
                "Closed": Decimal(group.closed_vulnerabilities),
                "Temporarily Accepted": Decimal(group.accepted),
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
                ["Temporarily Accepted"]
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
                "Temporarily Accepted": TREATMENT.passive,
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
                    "Temporarily Accepted",
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
        percentageValues={
            "Closed": [
                percentage_value[0]["Closed"]
                for percentage_value in percentage_values
            ],
            "Temporarily Accepted": [
                percentage_value[0]["Temporarily Accepted"]
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
            "Temporarily Accepted": [
                percentage_value[1]["Temporarily Accepted"]
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
    async for org_id, _, org_groups in (
        utils.iterate_organizations_and_groups()
    ):
        utils.json_dump(
            document=format_data(
                data=await get_data_many_groups(list(org_groups)),
                limit=24,
            ),
            entity="organization",
            subject=org_id,
        )

    async for org_id, org_name, _ in utils.iterate_organizations_and_groups():
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
