from .schema import (
    CREDENTIALS,
)
from db_model.credentials.types import (
    Credentials,
    HttpsPatSecret,
    OauthAzureSecret,
    OauthBitbucketSecret,
    OauthGithubSecret,
    OauthGitlabSecret,
)
from decorators import (
    enforce_owner,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from roots.validations import (
    get_cred_token,
)
from typing import (
    Optional,
)


@CREDENTIALS.field("token")
@enforce_owner
async def resolve(
    parent: Credentials, info: GraphQLResolveInfo
) -> Optional[str]:
    if isinstance(parent.state.secret, HttpsPatSecret):
        return parent.state.secret.token

    if isinstance(
        parent.state.secret,
        (
            OauthGithubSecret,
            OauthBitbucketSecret,
            OauthAzureSecret,
            OauthGitlabSecret,
        ),
    ):
        return await get_cred_token(
            credential_id=parent.id,
            organization_id=parent.organization_id,
            loaders=info.context.loaders,
            credential=parent,
        )

    return None
