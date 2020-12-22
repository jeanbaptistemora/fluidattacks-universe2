# Standard
from typing import cast, Dict, List

# Third party
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend import util
from backend.decorators import (
    enforce_group_level_auth_async,
    get_entity_cache_async
)
from backend.domain import comment as comment_domain
from backend.typing import Comment, Finding


@enforce_group_level_auth_async
@get_entity_cache_async
async def resolve(
    parent: Finding,
    info: GraphQLResolveInfo,
    **_kwargs: None
) -> List[Comment]:
    finding_id: str = cast(Dict[str, str], parent)['id']
    group_name: str = cast(Dict[str, str], parent)['project_name']

    user_data: Dict[str, str] = await util.get_jwt_content(info.context)
    user_email: str = user_data['user_email']

    return await comment_domain.get_observations(
        group_name,
        finding_id,
        user_email
    )
