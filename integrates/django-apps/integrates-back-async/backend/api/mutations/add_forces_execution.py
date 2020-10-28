# Standard
from typing import Any, Optional

# Third party
from ariadne.utils import convert_kwargs_to_snake_case
from django.core.files.uploadedfile import InMemoryUploadedFile
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend import util
from backend.decorators import enforce_group_level_auth_async
from backend.domain import forces as forces_domain
from backend.typing import SimplePayload


@convert_kwargs_to_snake_case
@enforce_group_level_auth_async
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    project_name: str,
    log: Optional[InMemoryUploadedFile] = None,
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
