from datetime import datetime
from graphql.type.definition import GraphQLResolveInfo

from db_model.findings.types import Finding
from newutils import datetime as datetime_utils


def resolve(
    parent: Finding, _info: GraphQLResolveInfo, **_kwargs: None
) -> str:
    release_date = ""
    if parent.approval:
        date = datetime.fromisoformat(parent.approval.modified_date)
        release_date = datetime_utils.get_as_str(date)
    return release_date
