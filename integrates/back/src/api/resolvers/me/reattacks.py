from db_model.vulnerabilities.types import (
    VulnerabilitiesConnection,
    VulnerabilityEdge,
)
from db_model.vulnerabilities.utils import (
    filter_non_zero_risk,
    format_vulnerability,
)
from decorators import (
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from search.operations import (
    search,
)
from typing import (
    Any,
)


@require_login
async def resolve(
    _parent: dict[str, Any],
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> VulnerabilitiesConnection:

    results = await search(
        must_filters=[
            {"state.status": "OPEN"},
            {"verification.status": "REQUESTED"},
        ],
        index="vulnerabilities",
        limit=100,
    )

    vulnerabilities = filter_non_zero_risk(
        tuple(format_vulnerability(result) for result in results.items)
    )

    return VulnerabilitiesConnection(
        edges=tuple(
            VulnerabilityEdge(
                cursor=results.page_info.end_cursor,
                node=vulnerability,
            )
            for vulnerability in vulnerabilities
        ),
        page_info=results.page_info,
    )
