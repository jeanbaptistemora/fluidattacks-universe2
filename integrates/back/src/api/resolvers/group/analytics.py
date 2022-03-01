from analytics import (
    domain as analytics_domain,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from db_model.groups.types import (
    Group,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Any,
    Dict,
    Union,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    enforce_group_level_auth_async,
    require_asm,
)
async def resolve(
    parent: Union[Group, Dict[str, Any]],
    _info: GraphQLResolveInfo,
    **kwargs: str,
) -> object:
    group_name: str = (
        parent["name"] if isinstance(parent, dict) else parent.name
    )
    document_name: str = kwargs["document_name"]
    document_type: str = kwargs["document_type"]

    return await analytics_domain.get_document(
        document_name=document_name,
        document_type=document_type,
        entity="group",
        subject=group_name,
    )
