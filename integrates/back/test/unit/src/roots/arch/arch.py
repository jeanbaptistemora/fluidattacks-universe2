from arch_lint.dag import (
    DagMap,
)
from typing import (
    Dict,
    Tuple,
    Union,
)

_dag: Dict[str, Tuple[Union[Tuple[str, ...], str], ...]] = {
    "roots": ("domain", "validations", "utils", "types"),
}


def project_dag() -> DagMap:
    result = DagMap.new(_dag)
    if isinstance(result, Exception):
        raise result
    return result
