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
from decimal import (
    Decimal,
)
from typing import (
    cast,
    Dict,
    Iterable,
    List,
    Union,
)


@alru_cache(maxsize=None, typed=True)
async def get_group_document(group: str) -> Dict[str, Dict[datetime, float]]:
    data: List[GroupDocumentData] = []
    context = get_new_context()
    group_loader = context.group
    data_name = "remediated_over_time_cvssf"

    group_data = await group_loader.load(group)
    group_over_time = [elements[-12:] for elements in group_data[data_name]]

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
                    date=translate_date(accepted["x"]),
                    total=found["y"],
                )
            )

    return {
        "date": {datum.date: 0 for datum in data},
        "Closed": {datum.date: datum.closed for datum in data},
        "Accepted": {datum.date: datum.accepted for datum in data},
        "Open": {datum.date: datum.opened for datum in data},
    }


async def get_many_groups_document(
    groups: Iterable[str],
) -> Dict[str, Dict[datetime, float]]:
    group_documents = await collect(map(get_group_document, groups))

    all_dates: List[datetime] = sorted(
        set(
            date
            for group_document in group_documents
            for date in group_document["date"]
        )
    )

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
            "Open",
        ]
    }


def format_document(
    document: Dict[str, Dict[datetime, float]],
) -> dict:
    return dict(
        data=dict(
            x="date",
            columns=[
                cast(List[Union[Decimal, str]], [name])
                + [
                    date.strftime(DATE_FMT)
                    if name == "date"
                    else Decimal(document[name][date]).quantize(Decimal("0.1"))
                    for date in tuple(document["date"])[-12:]
                ]
                for name in document
            ],
            colors={
                "Closed": RISK.more_passive,
                "Accepted": RISK.agressive,
                "Open": RISK.more_agressive,
            },
            groups=[
                [
                    "Closed",
                    "Accepted",
                    "Open",
                ]
            ],
            type="bar",
            order=None,
            stack=dict(
                normalize=True,
            ),
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
                label=dict(
                    text="CVSSF",
                    position="inner-top",
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


if __name__ == "__main__":
    run(generate_all())
