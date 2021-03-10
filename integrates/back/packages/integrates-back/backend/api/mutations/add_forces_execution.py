# Standard
from typing import (
    Any,
    Optional,
)

# Third party
from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo
from starlette.datastructures import UploadFile

# Local
from backend import util
from backend.decorators import enforce_group_level_auth_async
from backend.typing import SimplePayload
from forces import domain as forces_domain


@convert_kwargs_to_snake_case  # type: ignore
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
        util.cloudwatch_log(
            info.context,
            (
                f'Security: Created forces execution in {project_name} '
                'project successfully'
            )
        )
    return SimplePayload(success=success)
