from .schema import (
    ME,
)
from dataloaders import (
    Dataloaders,
)
from db_model.events.types import (
    Event,
)
from db_model.events.utils import (
    filter_events_not_in_groups,
    format_event,
)
from db_model.groups.types import (
    Group,
)
from decorators import (
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from group_access.domain import (
    get_stakeholder_groups_names,
)
from more_itertools import (
    flatten,
)
from search.operations import (
    search,
)
from typing import (
    Any,
)


@ME.field("pendingEvents")
@require_login
async def resolve(
    parent: dict[str, Any],
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> list[Event]:
    user_email = str(parent["user_email"])
    results = await search(
        must_not_filters=[{"state.status": "SOLVED"}],
        index="events",
        limit=1000,
    )
    loaders: Dataloaders = info.context.loaders
    test_groups: list[Group] = list(
        flatten(
            await loaders.organization_groups.load_many(
                [
                    "0d6d8f9d-3814-48f8-ba2c-f4fb9f8d4ffa",
                    "a23457e2-f81f-44a2-867f-230082af676c",
                ]
            )
        )
    )
    events_filtered = filter_events_not_in_groups(
        groups=test_groups,
        events=[format_event(result) for result in results.items],
    )
    stakeholder_groups = await get_stakeholder_groups_names(
        loaders, user_email, True
    )

    return [
        event
        for event in events_filtered
        if event.group_name in stakeholder_groups
    ]
