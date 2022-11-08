# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from azure.devops.v6_0.git.models import (
    GitCommit,
)
from azure_repositories.types import (
    CredentialsGitRepository,
    CredentialsGitRepositoryCommit,
)
from dataloaders import (
    Dataloaders,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Optional,
)


async def resolve(
    parent: CredentialsGitRepository,
    info: GraphQLResolveInfo,
) -> Optional[str]:
    loaders: Dataloaders = info.context.loaders
    git_commits: tuple[
        GitCommit, ...
    ] = await loaders.organization_integration_repositories_commits.load(
        CredentialsGitRepositoryCommit(
            credential=parent.credential,
            project_name=parent.repository.project.name,
            repository_id=parent.repository.id,
        )
    )

    if git_commits:
        return git_commits[0].committer.date

    return None
