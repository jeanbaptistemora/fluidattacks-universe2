from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    SimplePayload,
)
from db_model.organizations.types import (
    OrganizationPolicies,
)
from decimal import (
    Decimal,
)
from decorators import (
    enforce_organization_level_auth_async,
)
from dynamodb.types import (
    Item,
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
from typing import (
    Any,
)


@convert_kwargs_to_snake_case
@enforce_organization_level_auth_async
async def mutate(
    _parent: None, info: GraphQLResolveInfo, **parameters: Any
) -> SimplePayload:
    user_data = await token_utils.get_jwt_content(info.context)
    user_email = user_data["user_email"]
    new_policies = format_org_policies_to_update(parameters)

    organization_id = parameters.pop("organization_id")
    organization_name = parameters.pop("organization_name")
    success: bool = await orgs_domain.update_org_policies_typed(
        info.context.loaders,
        organization_id,
        organization_name,
        user_email,
        new_policies,
    )
    if success:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: User {user_email} updated policies for organization "
            f"{organization_name} with ID {organization_id}",
        )
    return SimplePayload(success=success)


def format_org_policies_to_update(item: Item) -> OrganizationPolicies:
    return OrganizationPolicies(
        max_acceptance_days=int(item["max_acceptance_days"])
        if item.get("max_acceptance_days") is not None
        else None,
        max_acceptance_severity=Decimal(
            item["max_acceptance_severity"]
        ).quantize(Decimal("0.1"))
        if item.get("max_acceptance_severity")
        else None,
        max_number_acceptances=int(item["max_number_acceptances"])
        if item.get("max_number_acceptances") is not None
        else None,
        min_acceptance_severity=Decimal(
            item["min_acceptance_severity"]
        ).quantize(Decimal("0.1"))
        if item.get("min_acceptance_severity")
        else None,
        min_breaking_severity=Decimal(item["min_breaking_severity"]).quantize(
            Decimal("0.1")
        )
        if item.get("min_breaking_severity")
        else None,
        vulnerability_grace_period=int(item["vulnerability_grace_period"])
        if item.get("vulnerability_grace_period") is not None
        else None,
    )
