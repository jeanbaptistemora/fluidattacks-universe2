# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from db_model.roots.types import (
    IPRoot,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


def resolve(parent: IPRoot, _info: GraphQLResolveInfo) -> str:
    return parent.state.address
