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
    OrganizationPoliciesToUpdate,
)
from decimal import (
    Decimal,
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
from typing import (
    Any,
)


def _format_policies_to_update(
    policies_data: dict[str, Any],
) -> OrganizationPoliciesToUpdate:
    return OrganizationPoliciesToUpdate(
        max_acceptance_days=int(policies_data["max_acceptance_days"])
        if policies_data.get("max_acceptance_days") is not None
        else None,
        max_acceptance_severity=Decimal(
            policies_data["max_acceptance_severity"]
        ).quantize(Decimal("0.1"))
        if policies_data.get("max_acceptance_severity")
        else None,
        max_number_acceptances=int(policies_data["max_number_acceptances"])
        if policies_data.get("max_number_acceptances") is not None
        else None,
        min_acceptance_severity=Decimal(
            policies_data["min_acceptance_severity"]
        ).quantize(Decimal("0.1"))
        if policies_data.get("min_acceptance_severity")
        else None,
        min_breaking_severity=Decimal(
            policies_data["min_breaking_severity"]
        ).quantize(Decimal("0.1"))
        if policies_data.get("min_breaking_severity")
        else None,
        vulnerability_grace_period=int(
            policies_data["vulnerability_grace_period"]
        )
        if policies_data.get("vulnerability_grace_period") is not None
        else None,
    )


@convert_kwargs_to_snake_case
@enforce_organization_level_auth_async
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    **kwargs: Any,
) -> SimplePayload:
    loaders: Dataloaders = info.context.loaders
    user_data = await token_utils.get_jwt_content(info.context)
    user_email = user_data["user_email"]
    organization_id = kwargs.pop("organization_id")
    organization_name = kwargs.pop("organization_name")
    policies_to_update = _format_policies_to_update(kwargs)
    success: bool = await orgs_domain.update_policies(
        loaders,
        organization_id,
        organization_name,
        user_email,
        policies_to_update,
    )
    if success:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: User {user_email} updated policies for organization "
            f"{organization_name} with ID {organization_id}",
        )
    return SimplePayload(success=success)
