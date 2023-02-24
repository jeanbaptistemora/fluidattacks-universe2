from .schema import (
    ORGANIZATION,
)
from db_model.organizations.types import (
    Organization,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@ORGANIZATION.field("maxNumberAcceptances")
def resolve(
    parent: Organization,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> int | None:
    return parent.policies.max_number_acceptances
