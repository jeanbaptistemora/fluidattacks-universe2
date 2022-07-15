from aioextensions import (
    collect,
    run,
)
from async_lru import (
    alru_cache,
)
from charts.colors import (
    RISK,
)
from charts.generators.bar_chart.exposed_by_groups import (
    format_max_value,
)
from charts.utils import (
    get_portfolios_groups,
    iterate_groups,
    iterate_organizations_and_groups,
    json_dump,
    TICK_ROTATION,
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
)
from newutils.datetime import (
    get_date_from_iso_str,
    get_now,
)
from operator import (
    attrgetter,
)
from typing import (
    Any,
    NamedTuple,
)


class EventsInfo(NamedTuple):
    name: str
    days: int


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(
    *, group: str, loaders: Dataloaders
) -> tuple[EventsInfo, ...]:
    events_group: tuple[Event, ...] = await loaders.group_events.load(group)

    return tuple(
        sorted(
            [
                EventsInfo(
                    days=(
                        get_now().date()
                        - get_date_from_iso_str(event.event_date)
                    ).days,
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
    *, data: tuple[EventsInfo, ...], x_label: str
) -> dict[str, Any]:
    limited_data = [group for group in data if group.days > 0][:18]

    return dict(
        data=dict(
            columns=[
                ["Open event days"]
                + [str(group.days) for group in limited_data],
            ],
            colors={
                "Open event days": RISK.neutral,
            },
            labels=None,
            type="bar",
        ),
        legend=dict(
            show=False,
        ),
        axis=dict(
            x=dict(
                categories=[group.name for group in limited_data],
                label=dict(
                    position="inner-right",
                    text=x_label,
                ),
                tick=dict(
                    multiline=False,
                    outer=False,
                    rotate=TICK_ROTATION,
                ),
                type="category",
            ),
            y=dict(
                label=dict(
                    position="inner-top",
                    text="Days open",
                ),
                min=0,
                padding=dict(
                    bottom=0,
                ),
            ),
        ),
        barChartYTickFormat=True,
        maxValue=format_max_value(limited_data),
    )


async def generate_all() -> None:
    loaders: Dataloaders = get_new_context()
    x_label_many_groups: str = "Group name"

    async for group in iterate_groups():
        json_dump(
            document=format_data(
                data=await get_data_one_group(
                    group=group,
                    loaders=loaders,
                ),
                x_label="Event ID",
            ),
            entity="group",
            subject=group,
        )

    async for org_id, _, org_groups in iterate_organizations_and_groups():
        json_dump(
            document=format_data(
                data=await get_data_many_groups(
                    groups=org_groups, loaders=loaders
                ),
                x_label=x_label_many_groups,
            ),
            entity="organization",
            subject=org_id,
        )

    async for org_id, org_name, _ in iterate_organizations_and_groups():
        for portfolio, groups in await get_portfolios_groups(org_name):
            json_dump(
                document=format_data(
                    data=await get_data_many_groups(
                        groups=tuple(groups), loaders=loaders
                    ),
                    x_label=x_label_many_groups,
                ),
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
            )


if __name__ == "__main__":
    run(generate_all())
