from aioextensions import (
    run,
)
from async_lru import (
    alru_cache,
)
from charts.colors import (
    RISK,
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
)
from groups.domain import (
    get_creation_date,
)
from newutils.datetime import (
    get_date_from_iso_str,
    get_now,
)
from operator import (
    attrgetter,
)
from typing import (
    NamedTuple,
)


class EventsAvailability(NamedTuple):
    available: int
    non_available: int


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(
    *, group_name: str, loaders: Dataloaders
) -> EventsAvailability:
    # group: Group = await loaders.group.load(group_name)
    creation_date: date = get_date_from_iso_str(
        await get_creation_date(loaders=loaders, group_name=group_name)
    )
    events_group: tuple[Event, ...] = await loaders.group_events.load(
        group_name
    )
    sorted_events: tuple[Event, ...] = tuple(
        sorted(events_group, key=attrgetter("event_date"))
    )
    group_days: int = (get_now().date() - creation_date).days
    current_date: date = get_now().date()
    events_dates: tuple[tuple[date, date], ...] = tuple(
        (get_date_from_iso_str(event.event_date), current_date)
        if event.state.status != EventStateStatus.SOLVED
        else (
            get_date_from_iso_str(event.event_date),
            get_date_from_iso_str(event.state.modified_date),
        )
        for event in sorted_events
    )

    open_range: list[tuple[date, date]] = []
    if events_dates:
        start, stop = events_dates[0][0], events_dates[0][1]
        for event in events_dates:
            if event[0] <= stop:
                stop = event[1]
            else:
                open_range.append((start, stop))
                start, stop = event[0], event[1]

        open_range.append((start, stop))

    open_event_days: int = sum(
        [(range[1] - range[0]).days for range in open_range]
    )

    return EventsAvailability(
        available=group_days - open_event_days,
        non_available=open_event_days,
    )


def format_data(*, data: EventsAvailability) -> dict:

    return dict(
        data=dict(
            columns=[
                ["available", data.available],
                ["non available", data.non_available],
            ],
            type="pie",
            colors={
                "available": RISK.agressive,
                "non available": RISK.passive,
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
    async for group in iterate_groups():
        json_dump(
            document=format_data(
                data=await get_data_one_group(
                    group_name=group, loaders=loaders
                ),
            ),
            entity="group",
            subject=group,
        )


if __name__ == "__main__":
    run(generate_all())
