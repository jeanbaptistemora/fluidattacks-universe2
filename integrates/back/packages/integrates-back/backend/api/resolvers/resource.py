import sys
from typing import Any, Union

from ariadne import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

from backend.typing import (
    DownloadFilePayload as DownloadFilePayloadType,
    SimplePayload as SimplePayloadType
)
from backend import util


def _clean_resources_cache(project_name: str) -> None:
    util.queue_cache_invalidation(
        # resource entity related
        f'environments*{project_name}',
        f'files*{project_name}',
        # project entity related
        f'has*{project_name}',
        f'deletion*{project_name}',
        f'tags*{project_name}',
        f'subscription*{project_name}',
    )


@convert_kwargs_to_snake_case  # type: ignore
async def resolve_resources_mutation(
    obj: Any,
    info: GraphQLResolveInfo,
    **parameters: Any
) -> Union[SimplePayloadType, DownloadFilePayloadType]:
    """Wrap resources mutations."""
    field = util.camelcase_to_snakecase(info.field_name)
    resolver_func = getattr(sys.modules[__name__], f'_do_{field}')
    return await resolver_func(obj, info, **parameters)
