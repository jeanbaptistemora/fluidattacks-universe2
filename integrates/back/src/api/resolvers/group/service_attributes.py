import authz
from custom_types import (
    Group,
)
from decorators import (
    enforce_group_level_auth_async,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
import newrelic.agent
from typing import (
    List,
)


@newrelic.agent.function_trace()
@enforce_group_level_auth_async
async def resolve(
    parent: Group, _info: GraphQLResolveInfo, **_kwargs: None
) -> List[str]:
    group_name: str = parent["name"]
    return sorted(await authz.get_group_service_attributes(group_name))
