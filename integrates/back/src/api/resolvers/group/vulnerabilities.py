from db_model.groups.types import (
    Group,
)
from db_model.vulnerabilities.types import (
    VulnerabilitiesConnection,
    VulnerabilityEdge,
)
from db_model.vulnerabilities.utils import (
    format_vulnerability,
)
from dynamodb.types import (
    PageInfo,
)
from graphql import (
    GraphQLResolveInfo,
)
import logging
from search.operations import (
    search,
)
from typing import (
    Any,
)

LOGGER = logging.getLogger(__name__)


async def resolve(
    parent: Group,
    info: GraphQLResolveInfo,
    **kwargs: Any,
) -> VulnerabilitiesConnection:
    query: str = kwargs.get("search", "")
    results = await search(
        exact_filters={"group_name": parent.name},
        query=query,
    )
    loaders = info.context.loaders
    draft_ids = tuple(
        draft.id for draft in await loaders.group_drafts.load(parent.name)
    )
    edges = tuple(
        VulnerabilityEdge(
            cursor="",
            node=format_vulnerability(result),
        )
        for result in results
        if result["finding_id"] not in draft_ids
    )

    return VulnerabilitiesConnection(
        edges=edges,
        page_info=PageInfo(has_next_page=False, end_cursor=""),
    )
