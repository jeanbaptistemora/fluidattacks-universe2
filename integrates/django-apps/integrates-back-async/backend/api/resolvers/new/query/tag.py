# Standard
from typing import Dict, List

# Third party
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend import util
from backend.decorators import require_login
from backend.domain import (
    organization as org_domain,
    tag as tag_domain,
    user as user_domain
)
from backend.exceptions import TagNotFound
from backend.typing import Tag


@require_login
async def resolve(
    _parent: None,
    info: GraphQLResolveInfo,
    **kwargs: str
) -> Tag:
    tag_name: str = kwargs['tag'].lower()

    user_data: Dict[str, str] = await util.get_jwt_content(info.context)
    user_email: str = user_data['user_email']
    user_groups: List[str] = await user_domain.get_projects(user_email)

    if user_groups:
        org_id: str = await org_domain.get_id_for_group(user_groups[0])
        org_name: str = await org_domain.get_name_by_id(org_id)

        allowed_tags: List[str] = await tag_domain.filter_allowed_tags(
            org_name,
            user_groups
        )

        if tag_name in allowed_tags:
            tag = await tag_domain.get_attributes(org_name, tag_name)

            return {
                'name': tag['tag'],
                'last_closing_vuln': tag['last_closing_date'],
                **tag
            }

    raise TagNotFound()
