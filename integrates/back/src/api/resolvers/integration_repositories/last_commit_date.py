from .schema import (
    INTEGRATION_REPOSITORIES,
)
from dataloaders import (
    Dataloaders,
)
from db_model.azure_repositories.types import (
    CredentialsGitRepository,
    CredentialsGitRepositoryCommit,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Optional,
)


@INTEGRATION_REPOSITORIES.field("lastCommitDate")
async def resolve(
    parent: CredentialsGitRepository,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Optional[str]:
    loaders: Dataloaders = info.context.loaders
    git_commits = (
        await loaders.organization_integration_repositories_commits.load(
            CredentialsGitRepositoryCommit(
                credential=parent.credential,
                project_name=parent.repository.project.name,
                repository_id=parent.repository.id,
            )
        )
    )

    if git_commits:
        return git_commits[0].committer.date

    return None
