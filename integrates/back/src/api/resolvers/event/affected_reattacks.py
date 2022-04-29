from aiodataloader import (
    DataLoader,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Any,
    Dict,
    List,
)


async def resolve(
    parent: Dict[str, Any],
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> List[Vulnerability]:
    event_id = str(parent["id"])

    event_vulns_loader: DataLoader = (
        info.context.loaders.event_vulnerabilities_loader
    )
    vulns = await event_vulns_loader.load((event_id))

    if vulns is None:
        return []
    return vulns
