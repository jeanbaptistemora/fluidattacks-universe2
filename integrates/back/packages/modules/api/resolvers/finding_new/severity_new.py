from typing import Dict

from graphql.type.definition import GraphQLResolveInfo

from model.findings.types import Finding
from newutils import utils


def resolve(
    parent: Finding, _info: GraphQLResolveInfo, **_kwargs: None
) -> Dict[str, float]:
    severity = {
        utils.snakecase_to_camelcase(key): float(value)
        for key, value in parent.severity._asdict().items()
    }

    return severity
