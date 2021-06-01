from aiodataloader import (
    DataLoader,
)
from custom_types import (
    Finding,
    Vulnerability,
)
from functools import (
    partial,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from redis_cluster.operations import (
    redis_get_or_set_entity_attr,
)
from typing import (
    cast,
    Dict,
    List,
    Optional,
)


async def resolve(
    parent: Finding, info: GraphQLResolveInfo, **kwargs: str
) -> List[Vulnerability]:
    vulnerabilities: List[Vulnerability] = await redis_get_or_set_entity_attr(
        partial(resolve_no_cache, parent, info, **kwargs),
        entity="finding",
        attr="vulnerabilities",
        id=cast(Dict[str, str], parent)["id"],
    )

    state: Optional[str] = kwargs.get("state")
    if state:
        vulnerabilities = [
            vulnerability
            for vulnerability in vulnerabilities
            if vulnerability["current_state"] == state
        ]
    return vulnerabilities


async def resolve_no_cache(
    parent: Finding, info: GraphQLResolveInfo, **_kwargs: str
) -> List[Vulnerability]:
    finding_id: str = cast(Dict[str, str], parent)["id"]
    finding_vulns_loader: DataLoader = info.context.loaders.finding_vulns_nzr
    vulns: List[Vulnerability] = await finding_vulns_loader.load(finding_id)
    return vulns
