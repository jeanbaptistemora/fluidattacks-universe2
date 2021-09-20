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
    **_kwargs: None,
) -> int:
    response: int = await redis_get_or_set_entity_attr(
        partial(resolve_no_cache, parent, info, **_kwargs),
        entity="finding",
        attr="age",
        id=cast(str, parent["id"]),
    )
    return response


async def resolve_no_cache(
    parent: Dict[str, Finding],
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> int:
    finding_id: str = cast(str, parent["id"])
    get_oldest_vulnerability_report_date = (
        await findings_domain.get_oldest_vulnerability_report_date(
            info.context.loaders, finding_id
        )
    )
    age = findings_domain.get_report_days(get_oldest_vulnerability_report_date)
    return age
