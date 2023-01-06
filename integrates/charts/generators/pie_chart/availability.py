from aioextensions import (
    run,
)
from async_lru import (
    alru_cache,
)
from charts.generators.common.colors import (
    RISK,
)
from charts.generators.pie_chart.common import (
    format_csv_data,
)
from charts.utils import (
    iterate_groups,
    json_dump,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    date,
)
from db_model.events.enums import (
    EventStateStatus,
)
from db_model.events.types import (
    Event,
    GroupEventsRequest,
)
from db_model.groups.types import (
    Group,
)
from newutils.datetime import (
    get_utc_now,
)
from operator import (
    attrgetter,
)
from typing import (
    NamedTuple,
)


class EventsAvailability(NamedTuple):
    available: int
    name: str
    non_available: int


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(
    *, group_name: str, loaders: Dataloaders
) -> EventsAvailability:
    current_date: date = get_utc_now().date()
    group: Group = await loaders.group.load(group_name)
    creation_date = group.created_date.date()
    events_group: tuple[Event, ...] = await loaders.group_events.load(
        GroupEventsRequest(group_name=group_name)
    )
    sorted_events: tuple[Event, ...] = tuple(
        sorted(events_group, key=attrgetter("event_date"))
    )
    group_days: int = (current_date - creation_date).days
    events_dates: tuple[tuple[date, date], ...] = tuple(
        (event.event_date.date(), current_date)
        if event.state.status != EventStateStatus.SOLVED
        else (
            event.event_date.date(),
            event.state.modified_date.date(),
        )
        for event in sorted_events
    )

    open_range: list[tuple[date, date]] = []
    if events_dates:
        start, stop = events_dates[0][0], events_dates[0][1]
        for event in events_dates:
            if event[0] <= stop:
                stop = event[1] if stop < event[1] else stop
            else:
                open_range.append((start, stop))
                start, stop = event[0], event[1]

        open_range.append((start, stop))

    open_event_days: int = sum(
        (range[1] - range[0]).days for range in open_range
    )

    return EventsAvailability(
        available=group_days - open_event_days
        if group_days > open_event_days
        else 0,
        name=group_name,
        non_available=open_event_days,
    )


def format_data(*, data: EventsAvailability) -> dict:

    return dict(
        data=dict(
            columns=[
                ["Available", data.available],
                ["Unavailable", data.non_available],
            ],
            type="pie",
            colors={
                "Available": RISK.agressive,
                "Unavailable": RISK.passive,
            },
        ),
        legend=dict(
            position="right",
        ),
        pie=dict(
            label=dict(
                show=True,
            ),
        ),
    )


async def generate_all() -> None:
    loaders: Dataloaders = get_new_context()
    headers: list[str] = ["Group availability", "Days"]
    async for group in iterate_groups():
        document = format_data(
            data=await get_data_one_group(group_name=group, loaders=loaders),
        )
        json_dump(
            document=document,
            entity="group",
            subject=group,
            csv_document=format_csv_data(document=document, header=headers),
        )


if __name__ == "__main__":
    run(generate_all())
