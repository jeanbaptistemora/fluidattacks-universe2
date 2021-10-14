from db_model.findings.types import (
    Finding,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    utils,
)
from typing import (
    Dict,
)


def resolve(
    parent: Finding, _info: GraphQLResolveInfo, **_kwargs: None
) -> Dict[str, float]:
    severity = {
        utils.snakecase_to_camelcase(key): float(value)
        for key, value in parent.severity._asdict().items()
    }

    return severity
