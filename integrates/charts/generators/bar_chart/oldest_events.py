from aioextensions import (
    collect,
    run,
)
from async_lru import (
    alru_cache,
)
from charts.generators.bar_chart.utils import (
    format_data_csv,
    LIMIT,
)
from charts.generators.bar_chart.utils_top_vulnerabilities_by_source import (
    format_max_value,
)
from charts.generators.common.colors import (
    OTHER_COUNT,
)
from charts.utils import (
    CsvData,
    get_portfolios_groups,
    iterate_groups,
    iterate_organizations_and_groups,
    json_dump,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.events.enums import (
    EventStateStatus,
)
from db_model.events.types import (
    Event,
    GroupEventsRequest,
)
from decimal import (
    Decimal,
)
from newutils.datetime import (
    get_utc_now,
)
from operator import (
    attrgetter,
)
from typing import (
    NamedTuple,
    Optional,
)


class EventsInfo(NamedTuple):
    name: str
    days: int


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(
    *, group: str, loaders: Dataloaders
) -> tuple[EventsInfo, ...]:
    events_group: tuple[Event, ...] = await loaders.group_events.load(
        GroupEventsRequest(group_name=group)
    )

    return tuple(
        sorted(
            [
                EventsInfo(
                    days=(get_utc_now().date() - event.event_date.date()).days,
                    name=event.id,
                )
                for event in events_group
                if event.state.status != EventStateStatus.SOLVED
            ],
            key=attrgetter("days"),
            reverse=True,
        )
    )


async def get_data_many_groups(
    *,
    groups: tuple[str, ...],
    loaders: Dataloaders,
) -> tuple[EventsInfo, ...]:
    groups_data: tuple[tuple[EventsInfo, ...], ...] = await collect(
        tuple(
            get_data_one_group(group=group, loaders=loaders)
            for group in groups
        ),
        workers=32,
    )
    groups_events: tuple[EventsInfo, ...] = tuple(
        EventsInfo(
            days=group[0].days if group else 0,
            name=name,
        )
        for group, name in zip(groups_data, groups)
    )

    return tuple(sorted(groups_events, key=attrgetter("days"), reverse=True))


def format_data(
    *, data: tuple[EventsInfo, ...], legend: str, x_label: Optional[str] = None
) -> tuple[dict, CsvData]:
    limited_data = [group for group in data if group.days > 0][:LIMIT]

    json_data: dict = dict(
        data=dict(
            columns=[
                [legend] + [str(group.days) for group in limited_data],
            ],
            colors={
                legend: OTHER_COUNT,
            },
            labels=None,
            type="bar",
        ),
        legend=dict(
            show=False,
        ),
        axis=dict(
            rotated=True,
            x=dict(
                categories=[group.name for group in limited_data],
                **(
                    dict(label=dict(text=x_label, position="outer-top"))
                    if x_label
                    else {}
                ),
                tick=dict(
                    multiline=False,
                    outer=False,
                    rotate=0,
                ),
                type="category",
            ),
            y=dict(
                label=dict(
                    position="outer-top",
                    text="Days open",
                ),
                min=0,
                padding=dict(
                    bottom=0,
                ),
            ),
        ),
        exposureTrendsByCategories=True,
        keepToltipColor=True,
        barChartYTickFormat=True,
        maxValue=format_max_value(
            [(ldata.name, Decimal(ldata.days)) for ldata in limited_data]
        ),
    )

    csv_data = format_data_csv(
        header_value=str(json_data["data"]["columns"][0][0]),
        values=[Decimal(group.days) for group in data],
        categories=[group.name for group in data],
        header_title=x_label if x_label else "Group name",
    )

    return (json_data, csv_data)


async def generate_all() -> None:
    loaders: Dataloaders = get_new_context()
    legend_many_groups: str = "Days since the group is failing"

    async for group in iterate_groups():
        json_document, csv_document = format_data(
            data=await get_data_one_group(group=group, loaders=loaders),
            legend="Days since the event was reported",
            x_label="Event ID",
        )
        json_dump(
            document=json_document,
            entity="group",
            subject=group,
            csv_document=csv_document,
        )

    async for org_id, _, org_groups in iterate_organizations_and_groups():
        json_document, csv_document = format_data(
            data=await get_data_many_groups(
                groups=org_groups, loaders=loaders
            ),
            legend=legend_many_groups,
        )
        json_dump(
            document=json_document,
            entity="organization",
            subject=org_id,
            csv_document=csv_document,
        )

    async for org_id, org_name, _ in iterate_organizations_and_groups():
        for portfolio, groups in await get_portfolios_groups(org_name):
            json_document, csv_document = format_data(
                data=await get_data_many_groups(
                    groups=tuple(groups), loaders=loaders
                ),
                legend=legend_many_groups,
            )
            json_dump(
                document=json_document,
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
                csv_document=csv_document,
            )


if __name__ == "__main__":
    run(generate_all())
