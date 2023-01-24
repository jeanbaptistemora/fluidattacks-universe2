from db_model.azure_repositories.types import (
    CredentialsGitRepository,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from urllib.parse import (
    unquote_plus,
)


async def resolve(
    parent: CredentialsGitRepository,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> str:
    return unquote_plus(parent.repository.web_url)
