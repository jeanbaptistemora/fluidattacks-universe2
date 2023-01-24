from db_model.azure_repositories.types import (
    CredentialsGitRepository,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


async def resolve(
    parent: CredentialsGitRepository,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> str:
    return (
        parent.repository.default_branch
        if parent.repository.default_branch is not None
        else ""
    )
