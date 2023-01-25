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
    "app": ("app", "views", "middleware", "utils"),
    "app.views": ("charts", "evidence", "oauth", "auth"),
}


def project_dag() -> DagMap:
    return cast(DagMap, DagMap.new(_dag))
