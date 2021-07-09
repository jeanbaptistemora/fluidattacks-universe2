from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    SimplePayload,
)
from decorators import (
    enforce_group_level_auth_async,
)
from forces import (
    domain as forces_domain,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    logs as logs_utils,
)
from newutils.utils import (
    clean_up_kwargs,
    get_key_or_fallback,
)
from starlette.datastructures import (
    UploadFile,
)
from typing import (
    Any,
    Optional,
)


@convert_kwargs_to_snake_case
@enforce_group_level_auth_async
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    log: Optional[UploadFile] = None,
    **parameters: Any,
) -> SimplePayload:
    # Compatibility with old API
    group_name: str = get_key_or_fallback(parameters)
    parameters = clean_up_kwargs(parameters)
    success = await forces_domain.add_forces_execution(
        group_name=group_name, log=log, **parameters
    )
    if success:
        logs_utils.cloudwatch_log(
            info.context,
            (
                f"Security: Created forces execution in {group_name} "
                "group successfully"
            ),
        )
    return SimplePayload(success=success)
