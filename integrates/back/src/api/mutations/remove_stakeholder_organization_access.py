# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from api.mutations import (
    SimplePayload,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
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

    await orgs_domain.remove_access(
        info.context.loaders,
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
