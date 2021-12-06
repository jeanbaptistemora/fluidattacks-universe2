from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    SimplePayload,
)
from db_model.roots.types import (
    GitRootItem,
)
from decorators import (
    concurrent_decorators,
    enforce_user_level_auth_async,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from roots import (
    domain as roots_domain,
)
from typing import (
    Any,
    Dict,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_user_level_auth_async,
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    group_name: str,
    root_nickname: str,
    job_id: str,
    **kwargs: Any,
) -> SimplePayload:
    result = False
    root_nicknames: Dict[str, str] = {
        root.state.nickname: root.id
        for root in await info.context.loaders.group_roots.load(group_name)
        if isinstance(root, GitRootItem)
    }
    if root_id := root_nicknames.get(root_nickname):
        result = roots_domain.add_machine_execution(root_id, job_id, **kwargs)

    return SimplePayload(success=result)
