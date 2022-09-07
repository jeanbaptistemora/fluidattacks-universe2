# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from api.mutations import (
    SimplePayload,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from billing import (
    domain as billing_domain,
)
from db_model.organizations.types import (
    Organization,
)
from decorators import (
    concurrent_decorators,
    enforce_organization_level_auth_async,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    token as token_utils,
    validations,
)
from starlette.datastructures import (
    UploadFile,
)
from typing import (
    Any,
    Dict,
    Optional,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_organization_level_auth_async,
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    rut: Optional[UploadFile] = None,
    tax_id: Optional[UploadFile] = None,
    **kwargs: Any,
) -> SimplePayload:
    org: Organization = await info.context.loaders.organization.load(
        kwargs["organization_id"]
    )
    user_info: Dict[str, str] = await token_utils.get_jwt_content(info.context)
    user_email: str = user_info["user_email"]

    if rut is not None:
        validations.validate_sanitized_csv_input(
            rut.filename, rut.content_type
        )
    if tax_id is not None:
        validations.validate_sanitized_csv_input(
            tax_id.filename, tax_id.content_type
        )

    # Create payment method
    result: bool = await billing_domain.create_payment_method(
        org=org,
        user_email=user_email,
        card_number=kwargs["card_number"],
        card_expiration_month=kwargs["card_expiration_month"],
        card_expiration_year=kwargs["card_expiration_year"],
        card_cvc=kwargs["card_cvc"],
        make_default=kwargs["make_default"],
        business_name=kwargs["business_name"],
        city=kwargs["city"],
        country=kwargs["country"],
        email=kwargs["email"],
        state=kwargs["state"],
        rut=rut,
        tax_id=tax_id,
    )

    return SimplePayload(success=result)
