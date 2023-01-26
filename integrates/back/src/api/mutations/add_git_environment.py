from api.mutations import (
    SimplePayload,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_exceptions import (
    InvalidRootType,
)
from dataloaders import (
    Dataloaders,
)
from db_model.roots.types import (
    GitRoot,
    Root,
    RootRequest,
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
)
from roots import (
    domain as roots_domain,
)
from typing import (
    Optional,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login, enforce_group_level_auth_async, require_service_white
)
async def mutate(  # pylint: disable = too-many-arguments
    _parent: None,
    info: GraphQLResolveInfo,
    group_name: str,
    url: str,
    url_type: str,
    root_id: str,
    cloud_name: Optional[str] = None,
    **_kwargs: None,
) -> SimplePayload:
    loaders: Dataloaders = info.context.loaders
    root: Root = await loaders.root.load(RootRequest(group_name, root_id))
    if not isinstance(root, GitRoot):
        raise InvalidRootType()
    await roots_domain.add_root_environment_url(
        loaders=loaders,
        group_name=group_name,
        root_id=root_id,
        url=url,
        url_type=url_type,
        cloud_type=cloud_name,
    )
    logs_utils.cloudwatch_log(
        info.context, f"Security: Updated git envs for root {root_id}"
    )

    return SimplePayload(success=True)
