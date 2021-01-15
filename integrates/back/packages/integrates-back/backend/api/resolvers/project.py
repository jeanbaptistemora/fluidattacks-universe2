# Standard library  # pylint:disable=cyclic-import
# pylint:disable=too-many-lines
import sys
from typing import Any

# Third party libraries
from ariadne import (
    convert_kwargs_to_snake_case,
)
from graphql.type.definition import GraphQLResolveInfo

# Local libraries
from backend import util


@convert_kwargs_to_snake_case  # type: ignore
async def resolve_project_mutation(
        obj: Any,
        info: GraphQLResolveInfo,
        **parameters: Any) -> Any:
    """Wrap project mutations."""
    field = util.camelcase_to_snakecase(info.field_name)
    resolver_func = getattr(sys.modules[__name__], f'_do_{field}')
    return await resolver_func(obj, info, **parameters)
