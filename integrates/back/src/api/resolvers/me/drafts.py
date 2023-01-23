from dataloaders import (
    Dataloaders,
)
from db_model.findings.types import (
    Finding,
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
from group_access.domain import (
    get_stakeholder_groups_names,
)
from newutils.findings import (
    filter_findings_in_groups,
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
    parent: dict[str, Any],
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> tuple[Finding, ...]:
    user_email = str(parent["user_email"])
    results = await search(
        should_filters=[
            {"state.status": "CREATED"},
            {"state.status": "REJECTED"},
            {"state.status": "SUBMITTED"},
        ],
        must_not_filters=[
            {"state.status": "APPROVED"},
            {"state.status": "DELETED"},
            {"state.status": "MASKED"},
        ],
        index="findings",
        limit=500,
    )
    loaders: Dataloaders = info.context.loaders
    test_group_orgs = await loaders.organization_groups.load_many(
        (
            "0d6d8f9d-3814-48f8-ba2c-f4fb9f8d4ffa",
            "a23457e2-f81f-44a2-867f-230082af676c",
        )
    )
    org_filtered = filter_findings_non_in_test_orgs(
        test_group_orgs=tuple(test_group_orgs),
        findings=tuple(format_finding(result) for result in results.items),
    )
    stakeholder_groups = await get_stakeholder_groups_names(
        loaders, user_email, True
    )

    return tuple(
        filter_findings_in_groups(
            group_names=stakeholder_groups, findings=org_filtered
        )
    )
