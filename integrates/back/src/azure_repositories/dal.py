# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from azure.devops.client import (
    AzureDevOpsAuthenticationError,
)
from azure.devops.connection import (
    Connection,
)
from azure.devops.released.git.git_client import (
    GitClient,
)
from azure.devops.v6_0.git.models import (
    GitRepository,
)
import logging
import logging.config
from msrest.authentication import (
    BasicAuthentication,
)
from settings import (
    LOGGING,
)

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)


def get_repositories(
    *, base_url: str, access_token: str
) -> tuple[GitRepository, ...]:
    credentials = BasicAuthentication("", access_token)
    connection = Connection(base_url=base_url, creds=credentials)
    try:
        git_client: GitClient = connection.clients.get_git_client()
        repositories: list[GitRepository] = git_client.get_repositories()
    except AzureDevOpsAuthenticationError as exc:
        LOGGER.exception(exc, extra=dict(extra=locals()))
        return tuple()
    else:
        return tuple(repositories)
