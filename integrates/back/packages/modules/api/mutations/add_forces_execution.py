
from typing import (
    Any,
    Optional,
)

from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo
from starlette.datastructures import UploadFile

from custom_types import SimplePayload
from decorators import enforce_group_level_auth_async
from forces import domain as forces_domain
from newutils import logs as logs_utils


@convert_kwargs_to_snake_case
@enforce_group_level_auth_async
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    project_name: str,
    log: Optional[UploadFile] = None,
    **parameters: Any
) -> SimplePayload:
    success = await forces_domain.add_forces_execution(
        project_name=project_name,
        log=log,
        **parameters
    )
    if success:
        logs_utils.cloudwatch_log(
            info.context,
            (
                f'Security: Created forces execution in {project_name} '
                'project successfully'
            )
        )
    return SimplePayload(success=success)
