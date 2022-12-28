from dataloaders import (
    Dataloaders,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
)
from db_model.vulnerabilities.types import (
    FindingVulnerabilitiesZrRequest,
    VulnerabilitiesConnection,
    VulnerabilityFilters,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils.vulnerabilities import (
    get_inverted_state_converted,
)
from typing import (
    Any,
    Optional,
)


async def resolve(
    parent: Finding,
    info: GraphQLResolveInfo,
    after: Optional[str] = None,
    first: Optional[int] = None,
    state: Optional[str] = None,
    **kwargs: Any,
) -> VulnerabilitiesConnection:
    loaders: Dataloaders = info.context.loaders

    return await loaders.finding_vulnerabilities_released_nzr_c.load(
        FindingVulnerabilitiesZrRequest(
            finding_id=parent.id,
            after=after,
            filters=VulnerabilityFilters(
                treatment_status=kwargs.get("treatment"),
                verification_status=kwargs.get("reattack"),
                where=kwargs.get("where"),
            ),
            first=first,
            paginate=True,
            state_status=VulnerabilityStateStatus[
                get_inverted_state_converted(state)
            ]
            if state
            else None,
        )
    )
