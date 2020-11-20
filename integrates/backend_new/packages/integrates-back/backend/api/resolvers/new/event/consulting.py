# Standard
from typing import cast, Dict, List

# Third party
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend import util
from backend.decorators import get_entity_cache_async
from backend.domain import comment as comment_domain
from backend.typing import Comment, Event


@get_entity_cache_async
async def resolve(
    parent: Event,
    info: GraphQLResolveInfo,
    **_kwargs: None
) -> List[Comment]:
    event_id: str = cast(str, parent['id'])
    group_name: str = cast(str, parent['project_name'])

    user_data: Dict[str, str] = await util.get_jwt_content(info.context)
    user_email: str = user_data['user_email']

    return await comment_domain.get_event_comments(
        group_name,
        event_id,
        user_email
    )
