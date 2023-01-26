from dataloaders import (
    Dataloaders,
)
from db_model.findings.types import (
    FindingEdge,
    FindingsConnection,
)
from db_model.findings.utils import (
    format_finding,
)
from decorators import (
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils.findings import (
    filter_findings_non_in_test_orgs,
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
    info: GraphQLResolveInfo,
    **kwargs: Any,
) -> FindingsConnection:
    not_zero_requested = {
        "unreliable_indicators.unreliable_verification_summary.requested": 0
    }
    results = await search(
        after=kwargs.get("after"),
        must_filters=[
            {"unreliable_indicators.unreliable_status": "VULNERABLE"},
        ],
        must_not_filters=[not_zero_requested],
        index="findings",
        limit=kwargs.get("first", 100),
    )
    loaders: Dataloaders = info.context.loaders
    test_group_orgs = await loaders.organization_groups.load_many(
        (
            "0d6d8f9d-3814-48f8-ba2c-f4fb9f8d4ffa",
            "a23457e2-f81f-44a2-867f-230082af676c",
        )
    )
    findings = filter_findings_non_in_test_orgs(
        tuple(test_group_orgs),
        tuple(format_finding(result) for result in results.items),
    )

    return FindingsConnection(
        edges=tuple(
            FindingEdge(
                cursor=results.page_info.end_cursor,
                node=finding,
            )
            for finding in findings
        ),
        page_info=results.page_info,
        total=results.total,
    )
