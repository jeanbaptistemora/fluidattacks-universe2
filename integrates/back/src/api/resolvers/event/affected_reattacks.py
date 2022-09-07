# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from aiodataloader import (
    DataLoader,
)
from db_model.events.types import (
    Event,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


async def resolve(
    parent: Event,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> list[Vulnerability]:
    event_id = parent.id
    event_vulns_loader: DataLoader = (
        info.context.loaders.event_vulnerabilities_loader
    )
    vulns = await event_vulns_loader.load((event_id))

    if vulns is None:
        return []
    return vulns
