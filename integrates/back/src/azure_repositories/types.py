# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from azure.devops.v6_0.git.models import (
    GitRepository,
)
from db_model.credentials.types import (
    Credentials,
)
from typing import (
    NamedTuple,
)


class CredentialsGitRepository(NamedTuple):
    credential: Credentials
    repository: GitRepository


class CredentialsGitRepositoryCommit(NamedTuple):
    credential: Credentials
    project_name: str
    repository_id: str
