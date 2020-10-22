# Standard
from typing import cast, Dict, List, Optional

# Third party
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.decorators import get_entity_cache_async
from backend.typing import Finding
from backend.utils import findings as finding_utils


@get_entity_cache_async
async def resolve(
    parent: Finding,
    info: GraphQLResolveInfo,
    **_kwargs: None
) -> List[Dict[object, object]]:
    finding_id: str = cast(Dict[str, str], parent)['id']
    group_name: str = cast(Dict[str, str], parent)['project_name']

    # Temporary while migrating finding resolvers
    finding = await info.context.loaders['finding'].load(finding_id)
    records_url: Optional[str] = cast(
        Dict[str, Dict[str, Optional[str]]], finding
    )['records']['url']

    if records_url:
        return await finding_utils.get_records_from_file(
            group_name,
            finding_id,
            records_url
        )

    return []
