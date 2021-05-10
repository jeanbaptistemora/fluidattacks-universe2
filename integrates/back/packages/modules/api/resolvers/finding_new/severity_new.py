# Standard
from typing import Dict

# Third party
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend import util
from model.findings.types import Finding


def resolve(
    parent: Finding,
    _info: GraphQLResolveInfo,
    **_kwargs: None
) -> Dict[str, float]:
    severity = {
        util.snakecase_to_camelcase(key): float(value)
        for key, value in parent.severity._asdict().items()
    }

    return severity
