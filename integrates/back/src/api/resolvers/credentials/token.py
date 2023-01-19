from db_model.credentials.types import (
    Credentials,
    HttpsPatSecret,
    OauthGithubSecret,
    OauthGitlabSecret,
)
from decorators import (
    enforce_owner,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils.datetime import (
    get_utc_now,
)
from oauth.gitlab import (
    get_token,
)
from typing import (
    Optional,
)


@enforce_owner
async def resolve(
    parent: Credentials, info: GraphQLResolveInfo
) -> Optional[str]:
    if isinstance(parent.state.secret, HttpsPatSecret):
        return parent.state.secret.token

    if isinstance(parent.state.secret, OauthGithubSecret):
        return parent.state.secret.access_token

    if isinstance(parent.state.secret, OauthGitlabSecret):
        if parent.state.secret.valid_until <= get_utc_now():
            return await get_token(
                credential=parent,
                loaders=info.context.loaders,
            )

        return parent.state.secret.access_token

    return None
