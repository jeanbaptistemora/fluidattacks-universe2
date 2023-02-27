from .schema import (
    FINDING,
)
from db_model.findings.types import (
    Finding,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    datetime as datetime_utils,
)


@FINDING.field("lastStateDate")
async def resolve(
    parent: Finding,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> str:
    return datetime_utils.get_as_str(parent.state.modified_date)
