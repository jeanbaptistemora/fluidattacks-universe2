from db_model.credentials.types import (
    Credentials,
    OauthAzureSecret,
    OauthGithubSecret,
    OauthGitlabSecret,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


def resolve(parent: Credentials, _info: GraphQLResolveInfo) -> str:
    if isinstance(parent.state.secret, OauthGithubSecret):
        return "GITHUB"

    if isinstance(parent.state.secret, OauthGitlabSecret):
        return "GITLAB"

    if isinstance(parent.state.secret, OauthAzureSecret):
        return "AZURE"

    return ""
