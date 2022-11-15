# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from azure_repositories.types import (
    CredentialsGitRepository,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from urllib.parse import (
    unquote_plus,
)


async def resolve(
    parent: CredentialsGitRepository,
    _info: GraphQLResolveInfo,
) -> str:
    return unquote_plus(parent.repository.web_url)
