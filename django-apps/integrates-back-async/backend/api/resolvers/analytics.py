# Standard library
import asyncio
import sys
from typing import (
    Dict,
    List,
)

# Third party libraries
from ariadne import (
    convert_kwargs_to_snake_case,
    convert_camel_case_to_snake,
)

# Local libraries
from backend import (
    util,
)
from backend.decorators import (
    enforce_group_level_auth_async,
    get_entity_cache_async,
    require_integrates,
    require_login,
    require_project_access,
)
from backend.domain import (
    analytics as analytics_domain,
)
from backend.utils import (
    apm,
)


@apm.trace()
@enforce_group_level_auth_async
@require_integrates
@require_project_access
@get_entity_cache_async
async def _get_group_document(
    _, __, *,
    document_name: str,
    document_type: str,
    group_name: str,
):
    return await analytics_domain.get_document(
        document_name=document_name,
        document_type=document_type,
        level='group',
        subject=group_name,
    )


@apm.trace()
@require_login
@convert_kwargs_to_snake_case
async def resolve(context, info) -> Dict[str, object]:
    tasks: List[asyncio.Task] = []

    selected_fields: list = [
        selection
        for selection in info.field_nodes[0].selection_set.selections
        if not selection.name.value.startswith('_')
    ]

    for selection in selected_fields:
        field_name = \
            convert_camel_case_to_snake(selection.name.value)

        field_resolver = \
            getattr(sys.modules[__name__], f'_get_{field_name}')

        field_parameters = \
            util.get_field_parameters(selection, info.variable_values)

        tasks.append(asyncio.create_task(
            field_resolver(context, info, **field_parameters)
        ))

    return {
        convert_camel_case_to_snake(selection.name.value): result
        for selection, result in zip(
            selected_fields, await asyncio.gather(*tasks)
        )
    }
