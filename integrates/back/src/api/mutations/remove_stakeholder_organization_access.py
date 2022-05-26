from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    SimplePayload,
)
from dataloaders import (
    Dataloaders,
)
from db_model.organizations.types import (
    Organization,
)
from decorators import (
    enforce_organization_level_auth_async,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    logs as logs_utils,
    token as token_utils,
)
from organizations import (
    domain as orgs_domain,
)
from redis_cluster.operations import (
    redis_del_by_deps_soon,
)


@convert_kwargs_to_snake_case
@enforce_organization_level_auth_async
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    organization_id: str,
    user_email: str,
) -> SimplePayload:
    user_data = await token_utils.get_jwt_content(info.context)
    requester_email = user_data["user_email"]
    loaders: Dataloaders = info.context.loaders
    organization: Organization = await loaders.organization.load(
        organization_id
    )
    organization_name = organization.name

    success: bool = await orgs_domain.remove_user(
        info.context.loaders, organization_id, user_email.lower()
    )
    if success:
        info.context.loaders.organization_stakeholders.clear(organization_id)
        redis_del_by_deps_soon(
            "remove_stakeholder_organization_access",
            organization_id=organization_id,
        )
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Stakeholder {requester_email} removed stakeholder"
            f" {user_email} from organization {organization_name}",
        )
    else:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Stakeholder {requester_email} attempted to remove "
            f"stakeholder {user_email} from organization {organization_name}",
        )

    return SimplePayload(success=success)
