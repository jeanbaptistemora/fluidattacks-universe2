from arch_lint.dag import (
    DagMap,
)
from typing import (
    Dict,
    Tuple,
    Union,
)

_dag: Dict[str, Tuple[Union[Tuple[str, ...], str], ...]] = {
    "dynamodb": (
        "conditions",
        "operations_legacy",
        "keys",
        "operations",
        "utils",
        "model",
        "tables",
        "resource",
        "types",
        "exceptions",
    ),
}


def project_dag() -> DagMap:
    result = DagMap.new(_dag)
    if isinstance(result, Exception):
        raise result  # pylint: disable=raising-bad-type
    return result
