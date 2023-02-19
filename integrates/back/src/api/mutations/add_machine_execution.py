from .payloads.types import (
    SimplePayload,
)
from .schema import (
    MUTATION,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from dataloaders import (
    Dataloaders,
)
from db_model.roots.types import (
    GitRoot,
)
from decorators import (
    concurrent_decorators,
    enforce_user_level_auth_async,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from roots.domain import (
    add_machine_execution,
)
from typing import (
    Any,
)


@MUTATION.field("addMachineExecution")
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
    loaders: Dataloaders = info.context.loaders
    root_nicknames = {
        root.state.nickname: root.id
        for root in await loaders.group_roots.load(group_name)
        if isinstance(root, GitRoot)
    }
    result = False
    if root_id := root_nicknames.get(root_nickname):
        result = await add_machine_execution(root_id, job_id, **kwargs)

    return SimplePayload(success=result)
