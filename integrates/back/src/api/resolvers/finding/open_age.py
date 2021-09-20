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
) -> int:
    response: int = await redis_get_or_set_entity_attr(
        partial(resolve_no_cache, parent, info, **kwargs),
        entity="finding",
        attr="open_age",
        id=cast(str, parent["id"]),
    )
    return response


async def resolve_no_cache(
    parent: Dict[str, Finding], info: GraphQLResolveInfo, **_kwargs: None
) -> int:
    finding_id: str = cast(str, parent["id"])
    open_vulnerability_report_date = (
        await findings_domain.get_oldest_open_vulnerability_report_date(
            info.context.loaders, finding_id
        )
    )
    open_age = findings_domain.get_report_days(open_vulnerability_report_date)
    return open_age
