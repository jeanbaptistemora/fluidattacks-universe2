from .schema import (
    GIT_ROOT,
)
from db_model.roots.types import (
    GitRoot,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@GIT_ROOT.field("useVpn")
def resolve(parent: GitRoot, _info: GraphQLResolveInfo) -> bool:
    return parent.state.use_vpn
