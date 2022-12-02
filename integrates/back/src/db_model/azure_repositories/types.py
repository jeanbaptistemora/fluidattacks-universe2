from azure.devops.v6_0.git.models import (
    GitRepository,
)
from db_model.credentials.types import (
    Credentials,
)
from db_model.integration_repositories.types import (
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
