from .schema import (
    CREDENTIALS,
)
from db_model.credentials.types import (
    Credentials,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Optional,
)


@CREDENTIALS.field("azureOrganization")
def resolve(parent: Credentials, _info: GraphQLResolveInfo) -> Optional[str]:
    return parent.state.azure_organization
