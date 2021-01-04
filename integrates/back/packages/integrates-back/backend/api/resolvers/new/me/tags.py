# Standard
from typing import cast, List

# Third party
from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.decorators import require_organization_access
from backend.domain import (
    organization as org_domain,
    tag as tag_domain,
    user as user_domain
)
from backend.typing import Me, Tag


@convert_kwargs_to_snake_case  # type: ignore
@require_organization_access
async def resolve(
    parent: Me,
    _info: GraphQLResolveInfo,
    **kwargs: str
) -> List[Tag]:
    user_email: str = cast(str, parent['user_email'])

    organization_id: str = kwargs['organization_id']

    org_name = await org_domain.get_name_by_id(organization_id)
    org_tags = await tag_domain.get_tags(org_name)
    user_groups = await user_domain.get_projects(
        user_email,
        organization_id=organization_id
    )

    return [
        {
            'name': tag['tag'],
            'last_closing_vuln': tag['last_closing_date'],
            **tag
        }
        for tag in org_tags
        if any([
            group in user_groups
            for group in cast(List[str], tag['projects'])
        ])
    ]
