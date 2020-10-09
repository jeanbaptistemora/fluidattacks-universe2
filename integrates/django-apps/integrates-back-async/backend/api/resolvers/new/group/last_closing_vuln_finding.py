# Standard
from typing import cast, Optional

# Third party
from graphql.language.ast import SelectionSetNode
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.api.resolvers import finding as old_resolver
from backend.decorators import get_entity_cache_async, require_integrates
from backend.typing import Finding, Project as Group
from backend.utils import aio


@require_integrates
@get_entity_cache_async
async def resolve(
    parent: Group,
    info: GraphQLResolveInfo,
    **_kwargs: None
) -> Optional[Finding]:
    finding_id: str = cast(str, parent['last_closing_vuln_finding'])

    # Temporary while migrating finding resolvers
    if finding_id:
        finding = await old_resolver.resolve(
            info,
            finding_id,
            as_field=True,
            selection_set=cast(
                SelectionSetNode,
                info.field_nodes[0].selection_set
            )
        )
        return cast(Finding, await aio.materialize(finding))

    return None
