from .payloads.types import (
    SimplePayload,
)
from aioextensions import (
    collect,
)
from api import (
    APP_EXCEPTIONS,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from dataloaders import (
    Dataloaders,
)
from db_model.toe_inputs.types import (
    RootToeInputsRequest,
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
    **_kwargs: None,
) -> SimplePayload:
    loaders: Dataloaders = info.context.loaders
    user_info = await sessions_domain.get_jwt_content(info.context)
    user_email = user_info["user_email"]
    url = await remove_environment_url_id(
        loaders=loaders,
        root_id=root_id,
        url_id=url_id,
        user_email=user_email,
        group_name=group_name,
    )
    logs_utils.cloudwatch_log(
        info.context, f"Security: remove git envs {url_id} from root {root_id}"
    )

    try:
        inputs_to_update = await loaders.root_toe_inputs.load_nodes(
            RootToeInputsRequest(
                be_present=True,
                group_name=group_name,
                root_id=root_id,
            )
        )
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
    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Tried to update toe input for {(root_id, url_id)}",
        )
        raise

    return SimplePayload(success=True)
