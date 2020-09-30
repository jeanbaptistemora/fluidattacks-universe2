# Standard
from typing import cast, Dict, List

# Third party
from aiodataloader import DataLoader
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend import util
from backend.api.resolvers import project as old_resolver
from backend.domain import user as user_domain
from backend.typing import Organization, Project as Group
from backend.utils import aio


async def resolve(
    parent: Organization,
    info: GraphQLResolveInfo,
    **_kwargs: None
) -> List[Group]:
    user_info: Dict[str, str] = await util.get_jwt_content(info.context)
    user_email: str = user_info['user_email']
    org_id: str = cast(str, parent['id'])

    user_groups: List[str] = await user_domain.get_projects(
        user_email,
        organization_id=org_id
    )

    group_loader: DataLoader = info.context.loaders['group']
    groups: List[Group] = await group_loader.load_many(user_groups)

    # Temporary while migrating group resolvers
    return cast(
        List[Group],
        await aio.materialize(
            old_resolver.resolve(
                info,
                cast(Dict[str, str], group)['name'],
                selection_set=info.field_nodes[0].selection_set
            )
            for group in groups
        )
    )
