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
)


async def resolve(
    parent: Finding, info: GraphQLResolveInfo, **kwargs: None
) -> List[Vulnerability]:
    response: List[Vulnerability] = await redis_get_or_set_entity_attr(
        partial(resolve_no_cache, parent, info, **kwargs),
        entity="finding",
        attr="lines_vulnerabilities",
        id=cast(Dict[str, str], parent)["id"],
    )
    return response


async def resolve_no_cache(
    parent: Finding, info: GraphQLResolveInfo, **_kwargs: None
) -> List[Vulnerability]:
    finding_vulns_loader: DataLoader = info.context.loaders.finding_vulns
    finding_id: str = cast(Dict[str, str], parent)["id"]

    vulns: List[Vulnerability] = await finding_vulns_loader.load(finding_id)
    return [vuln for vuln in vulns if vuln["vuln_type"] == "lines"]
