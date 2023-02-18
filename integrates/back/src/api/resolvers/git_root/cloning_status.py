from .schema import (
    GIT_ROOT,
)
from db_model.roots.types import (
    GitRoot,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from roots.types import (
    GitRootCloningStatus,
)


@GIT_ROOT.field("cloningStatus")
def resolve(
    parent: GitRoot, _info: GraphQLResolveInfo
) -> GitRootCloningStatus:
    return GitRootCloningStatus(
        status=parent.cloning.status.value,
        message=parent.cloning.reason,
        commit=parent.cloning.commit,
    )
