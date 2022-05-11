from analytics import (
    domain as analytics_domain,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
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
from typing import (
    Any,
    Union,
)


@convert_kwargs_to_snake_case
@enforce_organization_level_auth_async
async def resolve(
    parent: Union[Organization, dict[str, Any]],
    _info: GraphQLResolveInfo,
    **kwargs: str,
) -> object:
    document_name: str = kwargs["document_name"]
    document_type: str = kwargs["document_type"]
    if isinstance(parent, dict):
        org_id: str = parent["id"]
    else:
        org_id = parent.id

    return await analytics_domain.get_document(
        document_name=document_name,
        document_type=document_type,
        entity="organization",
        subject=org_id,
    )
