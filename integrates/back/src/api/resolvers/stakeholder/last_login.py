from .schema import (
    STAKEHOLDER,
)
from db_model.stakeholders.types import (
    Stakeholder,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    datetime as datetime_utils,
)


@STAKEHOLDER.field("lastLogin")
def resolve(
    parent: Stakeholder,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> str | None:
    return (
        datetime_utils.get_as_str(parent.last_login_date)
        if parent.last_login_date
        else None
    )
