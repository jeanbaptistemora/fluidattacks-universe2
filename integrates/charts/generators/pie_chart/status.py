# Standard library
from typing import (
    Iterable,
    NamedTuple,
)

# Third party libraries
from aioextensions import (
    collect,
    run,
)
from async_lru import alru_cache

# Local libraries
from charts import utils
from charts.colors import RISK
from groups import domain as groups_domain


Status = NamedTuple(
    "Status",
    [
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
        open_vulnerabilities=item.get("open_vulnerabilities", 0),
        closed_vulnerabilities=item.get("closed_vulnerabilities", 0),
    )


async def get_data_many_groups(groups: Iterable[str]) -> Status:
    groups_data = await collect(map(get_data_one_group, groups))

    return Status(
        open_vulnerabilities=sum(
            [group.open_vulnerabilities for group in groups_data]
        ),
        closed_vulnerabilities=sum(
            [group.closed_vulnerabilities for group in groups_data]
        ),
    )


def format_document(data: Status) -> dict:
    return {
        "data": {
            "columns": [
                ["Closed", data.closed_vulnerabilities],
                ["Open", data.open_vulnerabilities],
            ],
            "type": "pie",
            "colors": {
                "Closed": RISK.more_passive,
                "Open": RISK.more_agressive,
            },
        },
        "legend": {
            "position": "right",
        },
        "pie": {
            "label": {
                "show": True,
            },
        },
    }


async def generate_all() -> None:
    async for group in utils.iterate_groups():
        utils.json_dump(
            document=format_document(
                data=await get_data_one_group(group),
            ),
            entity="group",
            subject=group,
        )

    async for org_id, _, org_groups in (
        utils.iterate_organizations_and_groups()
    ):
        utils.json_dump(
            document=format_document(
                data=await get_data_many_groups(org_groups),
            ),
            entity="organization",
            subject=org_id,
        )

    async for org_id, org_name, _ in (
        utils.iterate_organizations_and_groups()
    ):
        for portfolio, groups in await utils.get_portfolios_groups(org_name):
            utils.json_dump(
                document=format_document(
                    data=await get_data_many_groups(groups),
                ),
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
            )


if __name__ == "__main__":
    run(generate_all())
