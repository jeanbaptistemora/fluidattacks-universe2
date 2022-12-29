from aioextensions import (
    collect,
)
from api import (
    APP_EXCEPTIONS,
)
from api.mutations import (
    SimplePayload,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_exceptions import (
    InvalidBePresentFilterCursor,
)
from db_model.toe_inputs.types import (
    RootToeInputsRequest,
    ToeInput,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_login,
    require_service_white,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    logs as logs_utils,
)
from roots.domain import (
    remove_environment_url_id,
)
from sessions import (
    domain as sessions_domain,
)
from toe.inputs import (
    domain as toe_inputs_domain,
)
from toe.inputs.types import (
    ToeInputAttributesToUpdate,
)
from typing import (
    Any,
    Optional,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login, enforce_group_level_auth_async, require_service_white
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    group_name: str,
    root_id: str,
    url_id: str,
    **_kwargs: Any,
) -> SimplePayload:
    url: str = await remove_environment_url_id(
        loaders=info.context.loaders,
        root_id=root_id,
        url_id=url_id,
    )
    logs_utils.cloudwatch_log(
        info.context, f"Security: remove git envs {url_id} from root {root_id}"
    )
    user_info = await sessions_domain.get_jwt_content(info.context)
    user_email = user_info["user_email"]
    try:
        inputs_to_update: Optional[
            tuple[ToeInput, ...]
        ] = await info.context.loaders.root_toe_inputs.load_nodes(
            RootToeInputsRequest(
                be_present=True,
                group_name=group_name,
                root_id=root_id,
            )
        )

        if inputs_to_update:
            await collect(
                tuple(
                    toe_inputs_domain.update(
                        current_value=current_value,
                        attributes=ToeInputAttributesToUpdate(
                            be_present=False,
                        ),
                        modified_by=user_email,
                    )
                    for current_value in inputs_to_update
                    if current_value.component.startswith(url)
                )
            )

            logs_utils.cloudwatch_log(
                info.context,
                f"""Security: Updated toe input in {(root_id, url_id)}
                successfully""",
            )
        else:
            raise InvalidBePresentFilterCursor()

    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Tried to update toe input for {(root_id, url_id)}",
        )
        raise

    return SimplePayload(success=True)
