# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# None


from aiodataloader import (
    DataLoader,
)
from db_model.events.types import (
    Event,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    rename_kwargs,
    require_asm,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@rename_kwargs({"identifier": "event_id"})
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
@rename_kwargs({"event_id": "identifier"})
async def resolve(
    _parent: None, info: GraphQLResolveInfo, **kwargs: str
) -> Event:
    event_id: str = kwargs["identifier"]
    event_loader: DataLoader = info.context.loaders.event
    event: Event = await event_loader.load(event_id)

    return event
