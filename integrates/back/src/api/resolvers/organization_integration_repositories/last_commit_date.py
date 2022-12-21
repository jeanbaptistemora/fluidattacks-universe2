from db_model.integration_repositories.types import (
    OrganizationIntegrationRepository,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    datetime as datetime_utils,
)
from typing import (
    Optional,
)


async def resolve(
    parent: OrganizationIntegrationRepository,
    _info: GraphQLResolveInfo,
) -> Optional[str]:

    return (
        datetime_utils.get_as_str(parent.last_commit_date)
        if parent.last_commit_date
        else None
    )
