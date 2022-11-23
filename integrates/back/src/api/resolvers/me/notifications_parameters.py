from db_model.stakeholders.types import (
    NotificationsParameters,
    NotificationsPreferences,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


def resolve(
    parent: NotificationsPreferences,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> NotificationsParameters:
    return parent.parameters
