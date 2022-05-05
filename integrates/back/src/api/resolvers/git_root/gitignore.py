from db_model.roots.types import (
    GitRootItem,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


def resolve(parent: GitRootItem, _info: GraphQLResolveInfo) -> list[str]:
    return parent.state.gitignore
