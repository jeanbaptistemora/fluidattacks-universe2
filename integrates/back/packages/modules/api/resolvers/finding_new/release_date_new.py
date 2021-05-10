# Third party
from graphql.type.definition import GraphQLResolveInfo

# Local
from model.findings.types import Finding


def resolve(
    parent: Finding,
    _info: GraphQLResolveInfo,
    **_kwargs: None
) -> str:
    release_date = ''
    if parent.approval:
        release_date = parent.approval.modified_date

    return release_date
