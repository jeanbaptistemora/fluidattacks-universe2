# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from azure_repositories.types import (
    CredentialsGitRepository,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


async def resolve(
    parent: CredentialsGitRepository,
    _info: GraphQLResolveInfo,
) -> str:
    return parent.repository.web_url
