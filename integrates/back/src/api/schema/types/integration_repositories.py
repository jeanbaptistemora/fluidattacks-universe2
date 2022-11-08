# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from api.resolvers.integration_repositories import (
    default_branch,
    last_commit_date,
    url,
)
from ariadne import (
    ObjectType,
)

INTEGRATION_REPOSITORIES = ObjectType("IntegrationRepositories")
INTEGRATION_REPOSITORIES.set_field("defaultBranch", default_branch.resolve)
INTEGRATION_REPOSITORIES.set_field("lastCommitDate", last_commit_date.resolve)
INTEGRATION_REPOSITORIES.set_field("url", url.resolve)
