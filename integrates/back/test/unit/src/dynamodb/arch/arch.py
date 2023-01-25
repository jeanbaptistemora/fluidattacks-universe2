from arch_lint.dag import (
    DagMap,
)
from typing import (
    cast,
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
    return cast(DagMap, DagMap.new(_dag))
