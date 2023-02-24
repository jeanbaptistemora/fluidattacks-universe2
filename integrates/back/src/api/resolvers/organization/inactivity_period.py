from .schema import (
    ORGANIZATION,
)
from db_model.constants import (
    DEFAULT_INACTIVITY_PERIOD,
)
from db_model.organizations.types import (
    Organization,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@ORGANIZATION.field("inactivityPeriod")
def resolve(
    parent: Organization,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> int:
    return (
        parent.policies.inactivity_period
        if parent.policies.inactivity_period is not None
        else DEFAULT_INACTIVITY_PERIOD
    )
