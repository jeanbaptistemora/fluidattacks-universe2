# Standard libraries
from typing import (
    cast,
    List
)

# Third party libraries
from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local libraries
from backend.decorators import require_organization_access
from backend.domain import (
    user as user_domain
)
from backend.typing import (
    Me as MeType,
    Tag as TagType
)


@convert_kwargs_to_snake_case  # type: ignore
@require_organization_access
async def resolve(
    parent: MeType,
    info: GraphQLResolveInfo,
    **kwargs: str
) -> List[TagType]:
    organization_loader = info.context.loaders.organization
    organization_tags_loader = info.context.loaders.organization_tags
    user_email: str = cast(str, parent['user_email'])

    organization_id: str = kwargs['organization_id']

    organization = await organization_loader.load(organization_id)
    org_tags = await organization_tags_loader.load(organization['name'])
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
