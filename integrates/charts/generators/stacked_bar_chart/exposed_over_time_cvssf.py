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
    EXPOSED_OVER_TIME,
    sum_over_time_many_groups,
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
    Any,
    cast,
    Dict,
    Iterable,
    List,
    NamedTuple,
    Union,
)


class GroupDocumentCvssfData(NamedTuple):
    # pylint: disable=inherit-non-class, too-few-public-methods
    data_date: datetime
    low: Decimal
    medium: Decimal
    high: Decimal
    critical: Decimal


@alru_cache(maxsize=None, typed=True)
async def get_group_document(group: str) -> Dict[str, Dict[datetime, Decimal]]:
    data: List[GroupDocumentCvssfData] = []
    context = get_new_context()
    group_loader = context.group

    data_name = "exposed_over_time_cvssf"
    group_data = await group_loader.load(group)
    group_over_time = [elements[-12:] for elements in group_data[data_name]]

    if group_over_time:
        group_low_over_time = group_over_time[0]
        group_medium_over_time = group_over_time[1]
        group_high_over_time = group_over_time[2]
        group_critical_over_time = group_over_time[3]

        for low, medium, high, critical in zip(
            group_low_over_time,
            group_medium_over_time,
            group_high_over_time,
            group_critical_over_time,
        ):
            data.append(
                GroupDocumentCvssfData(
                    low=low["y"],
                    medium=medium["y"],
                    high=high["y"],
                    critical=critical["y"],
                    data_date=translate_date(low["x"]),
                )
            )

    return {
        "date": {datum.data_date: Decimal("0.0") for datum in data},
        "Exposure": {
            datum.data_date: Decimal(
                datum.low + datum.medium + datum.high + datum.critical
            )
            for datum in data
        },
    }


async def get_many_groups_document(
    groups: Iterable[str],
) -> Dict[str, Dict[datetime, Decimal]]:
    group_documents = await collect(map(get_group_document, groups))

    return sum_over_time_many_groups(group_documents, EXPOSED_OVER_TIME)


def format_document(
    document: Dict[str, Dict[datetime, Decimal]],
) -> Dict[str, Any]:
    return dict(
        data=dict(
            x="date",
            columns=[
                # pylint: disable=unsubscriptable-object
                cast(List[Union[Decimal, str]], [name])
                + [
                    date.strftime(DATE_FMT)
                    if name == "date"
                    else Decimal(document[name][date]).quantize(Decimal("0.1"))
                    for date in tuple(document["date"])[-12:]
                ]
                for name in document
            ],
            colors=dict(
                Exposure=RISK.more_agressive,
            ),
            type="area-spline",
            groups=[
                [
                    "Exposure",
                ]
            ],
            order=None,
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
            r=0,
        ),
        spline=dict(
            interpolation=dict(
                type="monotone",
            ),
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
