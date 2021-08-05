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
    DATE_FMT,
    GroupDocumentData,
    translate_date,
)
from dataloaders import (
    get_new_context,
)
from datetime import (
    datetime,
)
from typing import (
    cast,
    Dict,
    Iterable,
    List,
    Optional,
    Union,
)


@alru_cache(maxsize=None, typed=True)
async def get_group_document(
    group: str, days: Optional[int] = None
) -> Dict[str, Dict[datetime, float]]:
    data: List[GroupDocumentData] = []
    context = get_new_context()
    group_loader = context.group

    data_name = "remediated_over_time"
    if days == 30:
        data_name = f"{data_name}_30"
    elif days == 90:
        data_name = f"{data_name}_90"

    group_data = await group_loader.load(group)
    group_over_time = [
        # Last 12 weeks
        elements[-12:]
        for elements in group_data[data_name]
    ]

    if group_over_time:
        group_found_over_time = group_over_time[0]
        group_closed_over_time = group_over_time[1]
        group_accepted_over_time = group_over_time[2]

        for accepted, closed, found in zip(
            group_accepted_over_time,
            group_closed_over_time,
            group_found_over_time,
        ):
            data.append(
                GroupDocumentData(
                    accepted=accepted["y"],
                    closed=closed["y"],
                    opened=found["y"] - closed["y"] - accepted["y"],
                    date=translate_date(found["x"]),
                    total=found["y"],
                )
            )
    else:
        print(f"[WARNING] {group} has no remediated_over_time attribute")

    return {
        "date": {datum.date: 0 for datum in data},
        "Closed": {datum.date: datum.closed for datum in data},
        "Accepted": {datum.date: datum.accepted for datum in data},
        "Found": {
            datum.date: datum.closed + datum.accepted + datum.opened
            for datum in data
        },
    }


async def get_many_groups_document(
    groups: Iterable[str], days: Optional[int] = None
) -> Dict[str, Dict[datetime, float]]:
    group_documents = await collect(
        get_group_document(group, days) for group in groups
    )

    all_dates: List[datetime] = sorted(
        set(
            date
            for group_document in group_documents
            for date in group_document["date"]
        )
    )

    # fill missing dates with it's more near value to the left
    for group_document in group_documents:
        for name in group_document:
            last_date = None
            for date in all_dates:
                if date in group_document[name]:
                    last_date = date
                elif last_date:
                    group_document[name][date] = group_document[name][
                        last_date
                    ]
                else:
                    group_document[name][date] = 0

    return {
        name: {
            date: sum(
                group_document[name].get(date, 0)
                for group_document in group_documents
            )
            for date in all_dates
        }
        for name in [
            "date",
            "Closed",
            "Accepted",
            "Found",
        ]
    }


def format_document(document: Dict[str, Dict[datetime, float]]) -> dict:
    return dict(
        data=dict(
            x="date",
            columns=[
                cast(List[Union[float, str]], [name])
                + [
                    date.strftime(DATE_FMT)
                    if name == "date"
                    else document[name][date]
                    for date in tuple(document["date"])[-12:]
                ]
                for name in document
            ],
            colors={
                "Closed": RISK.more_passive,
                "Accepted": RISK.agressive,
                "Found": RISK.more_agressive,
            },
            types={
                "Closed": "line",
                "Accepted": "line",
                "Found": "line",
            },
        ),
        axis=dict(
            x=dict(
                tick=dict(
                    centered=True,
                    multiline=False,
                    rotate=12,
                ),
                type="category",
            ),
            y=dict(
                min=0,
                padding=dict(
                    bottom=0,
                ),
            ),
        ),
        grid=dict(
            x=dict(
                show=True,
            ),
            y=dict(
                show=True,
            ),
        ),
        legend=dict(
            position="bottom",
        ),
        point=dict(
            focus=dict(
                expand=dict(
                    enabled=True,
                ),
            ),
            r=5,
        ),
    )


async def generate_all() -> None:
    async for group in utils.iterate_groups():
        utils.json_dump(
            document=format_document(
                document=await get_group_document(group),
            ),
            entity="group",
            subject=group,
        )

    async for org_id, _, org_groups in (
        utils.iterate_organizations_and_groups()
    ):
        utils.json_dump(
            document=format_document(
                document=await get_many_groups_document(org_groups),
            ),
            entity="organization",
            subject=org_id,
        )

    async for org_id, org_name, _ in utils.iterate_organizations_and_groups():
        for portfolio, groups in await utils.get_portfolios_groups(org_name):
            utils.json_dump(
                document=format_document(
                    document=await get_many_groups_document(groups),
                ),
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
            )

    # Limit days
    list_days: List[int] = [30, 90]
    for days in list_days:
        async for group in utils.iterate_groups():
            utils.json_dump(
                document=format_document(
                    document=await get_group_document(group, days),
                ),
                entity="group",
                subject=f"{group}_{days}",
            )

        async for org_id, _, org_groups in (
            utils.iterate_organizations_and_groups()
        ):
            utils.json_dump(
                document=format_document(
                    document=await get_many_groups_document(org_groups, days),
                ),
                entity="organization",
                subject=f"{org_id}_{days}",
            )

        async for org_id, org_name, _ in (
            utils.iterate_organizations_and_groups()
        ):
            for portfolio, groups in await utils.get_portfolios_groups(
                org_name
            ):
                utils.json_dump(
                    document=format_document(
                        document=await get_many_groups_document(groups, days),
                    ),
                    entity="portfolio",
                    subject=f"{org_id}PORTFOLIO#{portfolio}_{days}",
                )


if __name__ == "__main__":
    run(generate_all())
