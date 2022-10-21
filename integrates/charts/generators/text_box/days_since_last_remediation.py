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
from charts import (
    utils,
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


@alru_cache(maxsize=None, typed=True)
async def generate_one(group: str) -> Decimal:
    loaders: Dataloaders = get_new_context()
    group_indicators: GroupUnreliableIndicators = (
        await loaders.group_unreliable_indicators.load(group)
    )

    return Decimal(group_indicators.last_closed_vulnerability_days or 0)


async def get_many_groups(groups: tuple[str, ...]) -> Decimal:
    groups_data = await collect(map(generate_one, groups), workers=32)

    return min(groups_data) if groups_data else Decimal("Infinity")


def format_data(last_closing_date: Decimal) -> dict:
    return {"fontSizeRatio": 0.5, "text": last_closing_date}


def format_csv_data(last_closing_date: Decimal) -> utils.CsvData:
    return utils.CsvData(
        headers=["Days since last remediation"],
        rows=[[str(last_closing_date)]],
    )


async def generate_all() -> None:
    last_closing_date: Decimal
    async for group in utils.iterate_groups():
        last_closing_date = await generate_one(group)
        utils.json_dump(
            document=format_data(last_closing_date=last_closing_date),
            entity="group",
            subject=group,
            csv_document=format_csv_data(last_closing_date=last_closing_date),
        )

    async for org_id, _, org_groups in (
        utils.iterate_organizations_and_groups()
    ):
        last_closing_date = await get_many_groups(org_groups)
        utils.json_dump(
            document=format_data(last_closing_date=last_closing_date),
            entity="organization",
            subject=org_id,
            csv_document=format_csv_data(last_closing_date=last_closing_date),
        )

    async for org_id, org_name, _ in utils.iterate_organizations_and_groups():
        for portfolio, groups in await utils.get_portfolios_groups(org_name):
            last_closing_date = await get_many_groups(tuple(groups))
            utils.json_dump(
                document=format_data(last_closing_date=last_closing_date),
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
                csv_document=format_csv_data(
                    last_closing_date=last_closing_date
                ),
            )


if __name__ == "__main__":
    run(generate_all())
