# Standard
from typing import cast

# Third party
from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local
from analytics import domain as analytics_domain
from backend.decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_integrates
)
from backend.typing import Project as Group


@convert_kwargs_to_snake_case  # type: ignore
@concurrent_decorators(
    enforce_group_level_auth_async,
    require_integrates,
)
async def resolve(
    parent: Group,
    _info: GraphQLResolveInfo,
    **kwargs: str
) -> object:
    group_name: str = cast(str, parent['name'])
    document_name: str = kwargs['document_name']
    document_type: str = kwargs['document_type']

    return await analytics_domain.get_document(
        document_name=document_name,
        document_type=document_type,
        entity='group',
        subject=group_name,
    )
