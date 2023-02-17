from .schema import (
    CREDENTIALS,
)
from db_model.credentials.types import (
    Credentials,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@CREDENTIALS.field("isPat")
def resolve(parent: Credentials, _info: GraphQLResolveInfo) -> bool:
    return parent.state.is_pat
