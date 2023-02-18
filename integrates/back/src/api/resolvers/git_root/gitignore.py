from .schema import (
    GIT_ROOT,
)
from db_model.roots.types import (
    GitRoot,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@GIT_ROOT.field("gitignore")
def resolve(parent: GitRoot, _info: GraphQLResolveInfo) -> list[str]:
    return parent.state.gitignore
