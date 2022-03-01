from aiodataloader import (
    DataLoader,
)
from custom_types import (
    Event,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    List,
)


async def resolve(
    parent: Event,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> List[Vulnerability]:
    event_id: str = parent["id"]

    event_vulns_loader: DataLoader = (
        info.context.loaders.event_vulnerabilities_loader
    )
    vulns = await event_vulns_loader.load((event_id))

    if vulns is None:
        return []
    return vulns
