from .payloads.types import (
    UpdateAccessTokenPayload,
)
from .schema import (
    MUTATION,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_exceptions import (
    InvalidExpirationTime,
)
from dataloaders import (
    Dataloaders,
)
from db_model.groups.types import (
    Group,
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
from groups import (
    domain as groups_domain,
)
from newutils import (
    datetime as datetime_utils,
    logs as logs_utils,
)
from sessions import (
    domain as sessions_domain,
)
from stakeholders import (
    domain as stakeholders_domain,
)


@MUTATION.field("updateForcesAccessToken")
@convert_kwargs_to_snake_case
@enforce_group_level_auth_async
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    group_name: str,
) -> UpdateAccessTokenPayload:
    loaders: Dataloaders = info.context.loaders
    user_info = await sessions_domain.get_jwt_content(info.context)
    responsible = user_info["user_email"]
    group: Group = await loaders.group.load(group_name)

    email = forces_domain.format_forces_email(group_name)
    if not await stakeholders_domain.exists(loaders, email):
        logs_utils.cloudwatch_log(
            info.context,
            (
                f'{user_info["user_email"]} try to update token for a user '
                f"forces that does not exist {email}"
            ),
        )
        return UpdateAccessTokenPayload(success=False, session_jwt="")

    expiration_time = int(
        datetime_utils.get_now_plus_delta(days=180).timestamp()
    )
    try:
        result = await groups_domain.update_forces_access_token(
            loaders=loaders,
            group_name=group_name,
            email=email,
            expiration_time=expiration_time,
            responsible=responsible,
        )
        if result:
            logs_utils.cloudwatch_log(
                info.context,
                (
                    f'{user_info["user_email"]} update access token for '
                    f"{group_name}"
                ),
            )
            await forces_domain.update_token(
                group_name=group_name,
                organization_id=group.organization_id,
                token=result,
            )
            logs_utils.cloudwatch_log(
                info.context,
                (
                    f'{user_info["user_email"]} store in secretsmanager '
                    f"forces token for {email}"
                ),
            )
            return UpdateAccessTokenPayload(success=True, session_jwt=result)

        logs_utils.cloudwatch_log(
            info.context,
            (
                f'{user_info["user_email"]} attempted to update access '
                f"token for {group_name}"
            ),
        )
        return UpdateAccessTokenPayload(success=False, session_jwt=result)

    except InvalidExpirationTime as exc:
        logs_utils.cloudwatch_log(
            info.context,
            (
                f'{user_info["user_email"]} attempted to use expiration time '
                "greater than six months or minor than current time"
            ),
        )
        raise exc
