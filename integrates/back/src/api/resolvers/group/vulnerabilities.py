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
    _info: GraphQLResolveInfo,
    **kwargs: Any,
) -> VulnerabilitiesConnection:
    query: str = kwargs.get("search", "")
    results = await search(
        exact_filters={"group_name": parent.name},
        query=query,
    )
    edges = tuple(
        VulnerabilityEdge(
            cursor="",
            node=format_vulnerability(result),
        )
        for result in results
        if result["group_name"] == parent.name
    )

    # Hopefully not needed, but we must ensure security with a new piece of
    # the stack
    if len(edges) != len(results):
        LOGGER.critical(
            "Exact filters mismatch",
            extra={"extra": {"group_name": parent.name, "query": query}},
        )

    return VulnerabilitiesConnection(
        edges=edges,
        page_info=PageInfo(has_next_page=False, end_cursor=""),
    )
