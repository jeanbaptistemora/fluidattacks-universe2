# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from db_model.roots.types import (
    Root,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


def resolve(parent: Root, _info: GraphQLResolveInfo) -> str:
    return parent.state.nickname
