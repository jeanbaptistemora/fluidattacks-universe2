# Standard
from typing import cast

# Third party
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.typing import (
    ExecutionVulnerabilities,
    ForcesExecution,
)
from forces import domain as forces_domain


async def resolve(
    parent: ForcesExecution,
    _info: GraphQLResolveInfo,
    **_kwargs: None
) -> ExecutionVulnerabilities:
    group_name: str = cast(str, parent['project_name'])
    execution_id: str = cast(str, parent['execution_id'])
    vulnerabilities: ExecutionVulnerabilities = cast(
        ExecutionVulnerabilities,
        parent.get('vulnerabilities', {})
    )

    return {
        **vulnerabilities,
        **await forces_domain.get_vulns_execution(group_name, execution_id)
    }
