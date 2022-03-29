from db_model.findings.types import (
    Finding,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils.findings import (
    get_formatted_evidence,
)
from typing import (
    Dict,
    Optional,
)


def resolve(
    parent: Finding, _info: GraphQLResolveInfo, **_kwargs: None
) -> Dict[str, Dict[str, Optional[str]]]:
    return get_formatted_evidence(parent)
