# Standard
from typing import cast, List

# Third party
from aiodataloader import DataLoader
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.decorators import require_integrates
from backend.typing import Finding, Project as Group


@require_integrates
async def resolve(
    parent: Group,
    info: GraphQLResolveInfo,
    **_kwargs: None
) -> int:
    group_name: str = cast(str, parent['name'])

    group_loader: DataLoader = info.context.loaders['project']
    finding_ids: List[str] = (await group_loader.load(group_name))['findings']

    finding_loader: DataLoader = info.context.loaders['finding']
    findings: List[Finding] = await finding_loader.load_many(finding_ids)

    return len(findings)
