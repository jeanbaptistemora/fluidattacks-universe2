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

ROOT = UnionType("Root")


@ROOT.type_resolver
def resolve_root_type(
    result: Root,
    _info: GraphQLResolveInfo,
    _return_type: GraphQLAbstractType,
) -> str | None:
    if isinstance(result, GitRoot):
        return "GitRoot"
    if isinstance(result, IPRoot):
        return "IPRoot"
    if isinstance(result, URLRoot):
        return "URLRoot"
    return None
