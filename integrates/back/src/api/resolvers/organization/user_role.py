import authz
from db_model.organizations.types import (
    Organization,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    token as token_utils,
)
from typing import (
    Any,
    Dict,
    Union,
)


async def resolve(
    parent: Union[Organization, dict[str, Any]],
    info: GraphQLResolveInfo,
    **kwargs: Dict[str, str],
) -> str:
    if isinstance(parent, dict):
        org_id: str = parent["id"]
    else:
        org_id = parent.id

    identifier = str(kwargs.get("identifier", org_id))

    user_info: Dict[str, str] = await token_utils.get_jwt_content(info.context)
    user_email: str = user_info["user_email"]

    return str(await authz.get_organization_level_role(user_email, identifier))
