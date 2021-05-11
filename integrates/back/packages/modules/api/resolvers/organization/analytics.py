
from typing import cast

from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

from analytics import domain as analytics_domain
from custom_types import Organization
from decorators import enforce_organization_level_auth_async


@convert_kwargs_to_snake_case
@enforce_organization_level_auth_async
async def resolve(
    parent: Organization,
    _info: GraphQLResolveInfo,
    **kwargs: str
) -> object:
    document_name: str = kwargs['document_name']
    document_type: str = kwargs['document_type']
    org_id: str = cast(str, parent['id'])

    return await analytics_domain.get_document(
        document_name=document_name,
        document_type=document_type,
        entity='organization',
        subject=org_id,
    )
