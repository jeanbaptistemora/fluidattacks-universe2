from ariadne import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    SimplePayload,
)
from decorators import (
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from groups import (
    domain as groups_domain,
)
from newutils import (
    token as token_utils,
)
from typing import (
    Any,
)


@require_login
@convert_kwargs_to_snake_case
async def mutate(
    _: Any,
    info: GraphQLResolveInfo,
    **kwargs: Any,
) -> SimplePayload:
    user_info = await token_utils.get_jwt_content(info.context)
    user_email = user_info["user_email"]
    group_names: list[str] = kwargs["group_names"]

    await groups_domain.request_upgrade(
        info.context.loaders, group_names, user_email
    )

    return SimplePayload(success=True)
