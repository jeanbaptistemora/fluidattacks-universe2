from .schema import (
    CREDENTIALS,
)
from db_model.credentials.types import (
    Credentials,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@CREDENTIALS.field("azureOrganization")
def resolve(parent: Credentials, _info: GraphQLResolveInfo) -> str | None:
    return parent.state.azure_organization
