# Standard
from typing import cast, Dict, List

# Third party
from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend import util
from backend.domain import (
    organization as org_domain,
    tag as tag_domain,
    user as user_domain
)
from backend.typing import Me, Tag


@convert_kwargs_to_snake_case
async def resolve(
    _parent: Me,
    info: GraphQLResolveInfo,
    **kwargs: str
) -> List[Tag]:
    user_info: Dict[str, str] = await util.get_jwt_content(info.context)
    user_email: str = user_info['user_email']

    organization_id: str = kwargs['organization_id']

    org_name = await org_domain.get_name_by_id(organization_id)
    org_tags = await tag_domain.get_tags(org_name, ['projects', 'tag'])
    user_groups = await user_domain.get_projects(
        user_email, organization_id=organization_id
    )
    tag_info = [
        {
            'name': str(tag['tag']),
            # Temporary while migrating tag resolvers
            'projects': [
                {'name': str(group)}
                for group in cast(List[str], tag['projects'])
            ]
        }
        for tag in org_tags
        if any([
            group in user_groups
            for group in cast(List[str], tag['projects'])
        ])
    ]

    return cast(List[Tag], tag_info)
