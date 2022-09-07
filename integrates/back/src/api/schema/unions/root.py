# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from ariadne import (
    UnionType,
)
from db_model.roots.types import (
    GitRoot,
    IPRoot,
    Root,
    URLRoot,
)
from graphql.type.definition import (
    GraphQLAbstractType,
    GraphQLResolveInfo,
)
from typing import (
    Optional,
)


def resolve_root_type(
    result: Root,
    _info: GraphQLResolveInfo,
    _return_type: GraphQLAbstractType,
) -> Optional[str]:
    if isinstance(result, GitRoot):
        return "GitRoot"
    if isinstance(result, IPRoot):
        return "IPRoot"
    if isinstance(result, URLRoot):
        return "URLRoot"
    return None


ROOT = UnionType("Root", resolve_root_type)
