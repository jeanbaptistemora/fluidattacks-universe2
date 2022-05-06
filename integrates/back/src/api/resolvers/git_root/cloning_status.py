from db_model.roots.types import (
    GitRootItem,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from roots.types import (
    GitRootCloningStatus,
)


def resolve(
    parent: GitRootItem, _info: GraphQLResolveInfo
) -> GitRootCloningStatus:
    return GitRootCloningStatus(
        status=parent.cloning.status.value,
        message=parent.cloning.reason,
        commit=parent.cloning.commit,
    )
