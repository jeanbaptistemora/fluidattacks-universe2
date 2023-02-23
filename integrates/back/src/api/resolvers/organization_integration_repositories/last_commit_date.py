from .schema import (
    ORGANIZATION_INTEGRATION_REPOSITORIES,
)
from db_model.integration_repositories.types import (
    OrganizationIntegrationRepository,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    datetime as datetime_utils,
)


@ORGANIZATION_INTEGRATION_REPOSITORIES.field("lastCommitDate")
async def resolve(
    parent: OrganizationIntegrationRepository,
    _info: GraphQLResolveInfo,
) -> str | None:

    return (
        datetime_utils.get_as_str(parent.last_commit_date)
        if parent.last_commit_date
        else None
    )
