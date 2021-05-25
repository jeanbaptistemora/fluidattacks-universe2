from functools import partial
from typing import List

from graphql.type.definition import GraphQLResolveInfo

from comments import domain as comments_domain
from custom_types import Comment
from db_model.findings.types import Finding
from redis_cluster.operations import redis_get_or_set_entity_attr
from newutils import token as token_utils


async def resolve(
    parent: Finding, info: GraphQLResolveInfo, **kwargs: None
) -> List[Comment]:
    response: List[Comment] = await redis_get_or_set_entity_attr(
        partial(resolve_no_cache, parent, info, **kwargs),
        entity="finding_new",
        attr="consulting_new",
        group=parent.group_name,
        id=parent.id,
    )
    return response


async def resolve_no_cache(
    parent: Finding, info: GraphQLResolveInfo, **_kwargs: None
) -> List[Comment]:
    user_data = await token_utils.get_jwt_content(info.context)
    user_email = user_data["user_email"]
    return await comments_domain.get_comments_new(
        parent.group_name, parent.id, user_email, info
    )
