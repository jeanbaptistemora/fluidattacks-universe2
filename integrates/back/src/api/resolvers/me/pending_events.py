from dataloaders import (
    Dataloaders,
)
from db_model.events.types import (
    Event,
)
from db_model.events.utils import (
    filter_event_non_in_test_orgs,
    filter_event_stakeholder_groups,
    format_event,
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
from search.operations import (
    search,
)
from typing import (
    Any,
)


@require_login
async def resolve(
    parent: dict[str, Any],
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> tuple[Event, ...]:
    user_email = str(parent["user_email"])
    results = await search(
        must_not_filters=[{"state.status": "SOLVED"}],
        index="events",
        limit=1000,
    )
    loaders: Dataloaders = info.context.loaders
    test_group_orgs = await loaders.organization_groups.load_many(
        (
            "0d6d8f9d-3814-48f8-ba2c-f4fb9f8d4ffa",
            "a23457e2-f81f-44a2-867f-230082af676c",
        )
    )
    org_filtered = filter_event_non_in_test_orgs(
        test_group_orgs=tuple(test_group_orgs),
        events=tuple(format_event(result) for result in results.items),
    )
    stakeholder_groups = await get_stakeholder_groups_names(
        loaders, user_email, True
    )

    return tuple(
        filter_event_stakeholder_groups(
            group_names=stakeholder_groups, events=org_filtered
        )
    )
