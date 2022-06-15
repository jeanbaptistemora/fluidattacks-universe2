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
from typing import (
    Any,
    Union,
)


async def resolve(
    parent: Union[dict[str, Any], Event],
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> list[Vulnerability]:
    if isinstance(parent, dict):
        event_id = str(parent["id"])
    else:
        event_id = parent.id
    event_vulns_loader: DataLoader = (
        info.context.loaders.event_vulnerabilities_loader
    )
    vulns = await event_vulns_loader.load(event_id)

    if vulns is None:
        return []
    return vulns
