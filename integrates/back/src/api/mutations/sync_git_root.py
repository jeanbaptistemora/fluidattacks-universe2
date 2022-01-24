from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from batch import (
    dal as batch_dal,
)
from custom_exceptions import (
    CredentialNotFound,
    InactiveRoot,
)
from custom_types import (
    SimplePayload,
)
from dataloaders import (
    Dataloaders,
)
from db_model.roots.types import (
    GitRootItem,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_login,
    require_service_white,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    logs as logs_utils,
    token as token_utils,
)
from typing import (
    Any,
    Dict,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_service_white,
)
async def mutate(
    _parent: None, info: GraphQLResolveInfo, **kwargs: Any
) -> SimplePayload:
    user_info: Dict[str, str] = await token_utils.get_jwt_content(info.context)
    user_email: str = user_info["user_email"]
    loaders: Dataloaders = info.context.loaders
    group_name = kwargs["group_name"]
    root: GitRootItem = await loaders.root.load(
        (group_name, kwargs["root_id"])
    )
    group_creds = await loaders.group_credentials.load(group_name)
    if root.state.status != "ACTIVE":
        raise InactiveRoot()
    if len(list(filter(lambda x: root.id in x.state.roots, group_creds))) == 0:
        raise CredentialNotFound()
    await batch_dal.put_action(
        action_name="clone_root",
        entity=root.group_name,
        subject=user_email,
        additional_info=root.state.nickname,
    )
    logs_utils.cloudwatch_log(
        info.context,
        f"Security: Queued a sync clone for root {root.state.nickname} in "
        f"{group_name} by {user_email}",
    )

    return SimplePayload(success=True)
