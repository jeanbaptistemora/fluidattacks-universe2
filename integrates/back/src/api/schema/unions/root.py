from ariadne import (
    UnionType,
)
from db_model.roots.types import (
    GitRootItem,
    IPRootItem,
    RootItem,
    URLRootItem,
)
from graphql.type.definition import (
    GraphQLAbstractType,
    GraphQLResolveInfo,
)
from typing import (
    Optional,
)


def resolve_root_type(
    result: RootItem,
    _info: GraphQLResolveInfo,
    _return_type: GraphQLAbstractType,
) -> Optional[str]:
    if isinstance(result, GitRootItem):
        return "GitRoot"
    if isinstance(result, IPRootItem):
        return "IPRoot"
    if isinstance(result, URLRootItem):
        return "URLRoot"
    return None


ROOT = UnionType("Root", resolve_root_type)
