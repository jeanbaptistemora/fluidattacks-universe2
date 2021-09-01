from custom_types import (
    Finding,
)
from findings import (
    domain as findings_domain,
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
)


async def resolve(
    parent: Dict[str, Finding],
    info: GraphQLResolveInfo,
    **kwargs: None,
) -> Dict[str, int]:
    response: Dict[str, int] = await redis_get_or_set_entity_attr(
        partial(resolve_no_cache, parent, info, **kwargs),
        entity="finding",
        attr="treatment_summary",
        id=cast(str, parent["id"]),
    )
    return response


async def resolve_no_cache(
    parent: Dict[str, Finding], info: GraphQLResolveInfo, **_kwargs: None
) -> Dict[str, int]:
    finding_id: str = cast(str, parent["id"])
    treatment_summary = await findings_domain.get_treatment_summary(
        info.context.loaders, finding_id
    )
    return {
        "accepted": treatment_summary.ACCEPTED,
        "accepted_undefined": treatment_summary.ACCEPTED_UNDEFINED,
        "in_progress": treatment_summary.IN_PROGRESS,
        "new": treatment_summary.NEW,
    }
