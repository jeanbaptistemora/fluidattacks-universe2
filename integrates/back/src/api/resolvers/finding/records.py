from custom_types import (
    Finding,
)
from findings.domain import (
    get_records_from_file,
)
from functools import (
    partial,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils.utils import (
    get_key_or_fallback,
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
    parent: Dict[str, Finding],
    info: GraphQLResolveInfo,
    **kwargs: None,
) -> List[Dict[object, object]]:
    response: List[Dict[object, object]] = await redis_get_or_set_entity_attr(
        partial(resolve_no_cache, parent, info, **kwargs),
        entity="finding",
        attr="records",
        id=cast(str, parent["id"]),
    )
    return response


async def resolve_no_cache(
    parent: Finding, _info: GraphQLResolveInfo, **_kwargs: None
) -> List[Dict[object, object]]:
    finding_id: str = cast(Dict[str, str], parent)["id"]
    group_name: str = get_key_or_fallback(cast(Dict[str, str], parent))
    records_url: Optional[str] = cast(
        Dict[str, Dict[str, Optional[str]]], parent
    )["records"]["url"]
    if records_url:
        return cast(
            List[Dict[object, object]],
            await get_records_from_file(group_name, finding_id, records_url),
        )
    return []
