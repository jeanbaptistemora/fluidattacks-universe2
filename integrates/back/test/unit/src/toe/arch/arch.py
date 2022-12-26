from arch_lint.dag import (
    DagMap,
)
from typing import (
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
    result = DagMap.new(_dag)
    if isinstance(result, Exception):
        raise result  # pylint: disable=raising-bad-type
    return result
