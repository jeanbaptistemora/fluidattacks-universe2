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
    format_stacked_percentages,
    RemediatedAccepted,
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
)


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(group: str) -> RemediatedAccepted:
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

    return RemediatedAccepted(
        group_name=group.lower(),
        accepted=treatment.get("accepted", 0),
        accepted_undefined=treatment.get("acceptedUndefined", 0),
        remaining_open_vulnerabilities=remaining_open_vulnerabilities
        if remaining_open_vulnerabilities >= 0
        else 0,
        open_vulnerabilities=open_vulnerabilities,
        closed_vulnerabilities=item.get("closed_vulnerabilities", 0),
    )


async def get_data_many_groups(groups: List[str]) -> List[RemediatedAccepted]:
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


def format_data(
    data: List[RemediatedAccepted], limit: int = 0
) -> Dict[str, Any]:
    limited_data = (
        list(
            sorted(
                data,
                key=lambda x: (
                    x.open_vulnerabilities
                    / (x.closed_vulnerabilities + x.open_vulnerabilities)
                    if (x.closed_vulnerabilities + x.open_vulnerabilities) > 0
                    else 0
                ),
                reverse=True,
            )
        )[:limit]
        if limit
        else list(data)
    )
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
    async for org_id, _, org_groups in (
        utils.iterate_organizations_and_groups()
    ):
        utils.json_dump(
            document=format_data(
                data=await get_data_many_groups(list(org_groups)),
                limit=18,
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
