# Standard
from functools import (
    partial,
)
from typing import cast, Dict, List, Optional

# Third party
from aiodataloader import DataLoader
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.decorators import enforce_group_level_auth_async
from backend.dal.helpers.redis import (
    redis_get_or_set_entity_attr,
)
from backend.typing import Finding, Vulnerability


@enforce_group_level_auth_async
async def resolve(
    parent: Finding,
    info: GraphQLResolveInfo,
    **kwargs: str
) -> List[Vulnerability]:
    zero_risk: List[Vulnerability] = await redis_get_or_set_entity_attr(
        partial(resolve_no_cache, parent, info, **kwargs),
        entity='finding',
        attr='zero_risk',
        id=cast(Dict[str, str], parent)['id'],
    )

    state: Optional[str] = kwargs.get('state')

    if state:
        zero_risk = [
            vulnerability
            for vulnerability in zero_risk
            if vulnerability['current_state'] == state
        ]

    return zero_risk


async def resolve_no_cache(
    parent: Finding,
    info: GraphQLResolveInfo,
    **_kwargs: str
) -> List[Vulnerability]:
    finding_id: str = cast(Dict[str, str], parent)['id']
    finding_vulns_loader: DataLoader = info.context.loaders.finding_vulns_zr
    zero_risk: List[Vulnerability] = await finding_vulns_loader.load(
        finding_id
    )

    return zero_risk
