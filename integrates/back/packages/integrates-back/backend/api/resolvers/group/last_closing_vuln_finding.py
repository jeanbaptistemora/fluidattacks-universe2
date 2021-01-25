# Standard
from typing import cast, Optional

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
) -> Optional[Finding]:
    finding_id: str = cast(str, parent['last_closing_vuln_finding'])

    if finding_id:
        finding_loader: DataLoader = info.context.loaders['finding']
        finding: Finding = await finding_loader.load(finding_id)

        return finding

    return None
