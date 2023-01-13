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
from starlette.datastructures import (
    UploadFile,
)
from typing import (
    Any,
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

    result: bool = await billing_domain.update_documents_new(
        org=org,
        payment_method_id=kwargs["payment_method_id"],
        business_name=kwargs["business_name"],
        city=kwargs["city"],
        country=kwargs["country"],
        email=kwargs["email"],
        state=kwargs["state"],
        rut=rut,
        tax_id=tax_id,
    )

    return SimplePayload(success=result)
