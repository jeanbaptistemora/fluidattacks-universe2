# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from api.resolvers.integration_repositories import (
    default_branch,
    last_commit_date,
    url,
)
from api.resolvers.organization_integration_repositories import (
    default_branch as organization_default_branch,
    last_commit_date as organization_last_commit_date,
    url as organization_url,
)
from ariadne import (
    ObjectType,
)

INTEGRATION_REPOSITORIES = ObjectType("IntegrationRepositories")
INTEGRATION_REPOSITORIES.set_field("defaultBranch", default_branch.resolve)
INTEGRATION_REPOSITORIES.set_field("lastCommitDate", last_commit_date.resolve)
INTEGRATION_REPOSITORIES.set_field("url", url.resolve)


ORGANIZATION_INTEGRATION_REPOSITORIES = ObjectType(
    "OrganizationIntegrationRepositories"
)
ORGANIZATION_INTEGRATION_REPOSITORIES.set_field(
    "defaultBranch", organization_default_branch.resolve
)
ORGANIZATION_INTEGRATION_REPOSITORIES.set_field(
    "lastCommitDate", organization_last_commit_date.resolve
)
ORGANIZATION_INTEGRATION_REPOSITORIES.set_field(
    "url", organization_url.resolve
)
