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
    "machine": (
        "availability",
        "jobs",
    ),
}


def project_dag() -> DagMap:
    return cast(DagMap, DagMap.new(_dag))
