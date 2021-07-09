from db_model.findings.types import (
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
    Dict,
    List,
)


async def resolve(
    parent: Finding, info: GraphQLResolveInfo, **kwargs: None
) -> List[Dict[object, object]]:
    response: List[Dict[object, object]] = await redis_get_or_set_entity_attr(
        partial(resolve_no_cache, parent, info, **kwargs),
        entity="finding",
        attr="records",
        id=parent.id,
    )
    return response


async def resolve_no_cache(
    parent: Finding, _info: GraphQLResolveInfo, **_kwargs: None
) -> List[Dict[object, object]]:
    records = []
    if parent.evidences.records:
        records = await findings_domain.get_records_from_file(
            parent.group_name, parent.id, parent.evidences.records.url
        )
    return records
