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
    "toe": ("lines", "ports", "inputs", "utils"),
    "toe.inputs": ("domain", "types"),
    "toe.ports": ("domain", "types"),
    "toe.lines": ("domain", "validations", "constants", "types", "utils"),
}


def project_dag() -> DagMap:
    return cast(DagMap, DagMap.new(_dag))
