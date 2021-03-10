# Standard
from typing import cast

# Third party
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.typing import ForcesExecution
from forces import domain as forces_domain


async def resolve(
    parent: ForcesExecution,
    _info: GraphQLResolveInfo,
    **_kwargs: None
) -> str:
    group_name: str = cast(str, parent['project_name'])
    execution_id: str = cast(str, parent['execution_id'])

    return cast(
        str,
        await forces_domain.get_log_execution(group_name, execution_id)
    )
