# Standard
# None

# Third party
from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend import util
from backend.decorators import enforce_group_level_auth_async
from backend.domain import user as user_domain
from backend.exceptions import InvalidExpirationTime
from backend.typing import UpdateAccessTokenPayload
from backend.utils import datetime as datetime_utils


@convert_kwargs_to_snake_case
@enforce_group_level_auth_async
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    project_name: str
) -> UpdateAccessTokenPayload:
    user_info = await util.get_jwt_content(info.context)

    user_email = user_domain.format_forces_user_email(project_name)
    if not user_domain.ensure_user_exists(user_email):
        util.cloudwatch_log(
            info.context,
            (
                f'{user_info["user_email"]} try to update token for a user '
                f'forces that does not exist {user_email}'
            )
        )
        return UpdateAccessTokenPayload(success=False, session_jwt='')

    expiration_time = int(
        datetime_utils.get_now_plus_delta(days=180).timestamp()
    )
    try:
        result = await user_domain.update_access_token(
            user_email,
            expiration_time,
        )
        if result.success:
            util.cloudwatch_log(
                info.context,
                (
                    f'{user_info["user_email"]} update access token for '
                    f'{user_email}'
                )
            )
        else:
            util.cloudwatch_log(
                info.context,
                (
                    f'{user_info["user_email"]} attempted to update access '
                    f'token for {user_email}'
                ),
            )
        return result
    except InvalidExpirationTime as exc:
        util.cloudwatch_log(
            info.context,
            (
                f'{user_info["user_email"]} attempted to use expiration time '
                'greater than six months or minor than current time'
            ),
        )
        raise exc
