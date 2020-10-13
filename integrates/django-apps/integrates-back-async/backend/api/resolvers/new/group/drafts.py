# Standard
from typing import cast, Dict, List

# Third party
from aiodataloader import DataLoader
from aioextensions import collect
from graphql.language.ast import SelectionSetNode
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.api.resolvers import finding as old_resolver
from backend.decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_integrates
)
from backend.typing import Finding, Project as Group


@concurrent_decorators(
    enforce_group_level_auth_async,
    require_integrates,
)
async def resolve(
    parent: Group,
    info: GraphQLResolveInfo,
    **_kwargs: None
) -> List[Finding]:
    group_name: str = cast(str, parent['name'])

    group_drafts_loader: DataLoader = info.context.loaders['group_drafts']
    draft_ids: List[str] = [
        finding['id']
        for finding in await group_drafts_loader.load(group_name)
    ]

    finding_loader: DataLoader = info.context.loaders['finding']
    drafts: List[Finding] = await finding_loader.load_many(draft_ids)

    return cast(
        List[Finding],
        await collect(
            old_resolver.resolve(
                info,
                cast(Dict[str, str], draft)['id'],
                as_field=True,
                selection_set=cast(
                    SelectionSetNode,
                    info.field_nodes[0].selection_set
                )
            )
            for draft in drafts
        )
    )
