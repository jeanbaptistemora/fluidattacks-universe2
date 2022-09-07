# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from db_model.roots.types import (
    GitRoot,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from roots.types import (
    GitRootCloningStatus,
)


def resolve(
    parent: GitRoot, _info: GraphQLResolveInfo
) -> GitRootCloningStatus:
    return GitRootCloningStatus(
        status=parent.cloning.status.value,
        message=parent.cloning.reason,
        commit=parent.cloning.commit,
    )
