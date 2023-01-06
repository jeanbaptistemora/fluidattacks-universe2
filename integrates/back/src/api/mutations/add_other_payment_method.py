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
from sessions import (
    domain as sessions_domain,
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
    user_info: Dict[str, str] = await sessions_domain.get_jwt_content(
        info.context
    )
    user_email: str = user_info["user_email"]

    # Create payment method
    result: bool = await billing_domain.create_other_payment_method(
        org=org,
        user_email=user_email,
        business_name=kwargs["business_name"],
        city=kwargs["city"],
        country=kwargs["country"],
        email=kwargs["email"],
        state=kwargs["state"],
        rut=rut,
        tax_id=tax_id,
    )

    return SimplePayload(success=result)
