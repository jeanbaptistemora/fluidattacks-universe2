from .payloads.types import (
    SimplePayload,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from dataloaders import (
    Dataloaders,
)
from decorators import (
    enforce_organization_level_auth_async,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    logs as logs_utils,
)
from organizations import (
    domain as orgs_domain,
    utils as orgs_utils,
)
from sessions import (
    domain as sessions_domain,
)


@convert_kwargs_to_snake_case
@enforce_organization_level_auth_async
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    organization_id: str,
    user_email: str,
) -> SimplePayload:
    user_data = await sessions_domain.get_jwt_content(info.context)
    requester_email = user_data["user_email"]
    loaders: Dataloaders = info.context.loaders
    organization = await orgs_utils.get_organization(loaders, organization_id)

    await orgs_domain.remove_access(
        organization_id,
        user_email.lower(),
        requester_email,
    )
    logs_utils.cloudwatch_log(
        info.context,
        f"Security: Stakeholder {requester_email} removed stakeholder"
        f" {user_email} from organization {organization.name}",
    )

    return SimplePayload(success=True)
