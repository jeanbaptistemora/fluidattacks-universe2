from azure.devops.v6_0.git.models import (
    GitRepository,
)
from datetime import (
    datetime,
)
from db_model.credentials.types import (
    Credentials,
)
from db_model.integration_repositories.types import (
    OrganizationIntegrationRepository,
    OrganizationIntegrationRepositoryConnection,
)
from typing import (
    NamedTuple,
    Optional,
)


class CredentialsGitRepository(NamedTuple):
    credential: Credentials
    repository: GitRepository


class CredentialsGitRepositoryCommit(NamedTuple):
    credential: Credentials
    project_name: str
    repository_id: str
    total: bool = False


class CredentialsGitRepositoryResolver(NamedTuple):
    credential: Optional[Credentials] = None
    repository: Optional[GitRepository] = None
    connection: Optional[OrganizationIntegrationRepositoryConnection] = None


class BasicRepoData(NamedTuple):
    id: str
    remote_url: str
    ssh_url: str
    web_url: str
    branch: str
    last_activity_at: datetime


class ProjectStats(NamedTuple):
    project: BasicRepoData
    commits: tuple[dict, ...]
    commits_count: int


class RepositoriesStats(NamedTuple):
    repositories: tuple[OrganizationIntegrationRepository, ...]
    missed_repositories: int
    missed_commits: int
