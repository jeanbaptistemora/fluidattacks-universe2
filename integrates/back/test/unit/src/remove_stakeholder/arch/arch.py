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
    "remove_stakeholder": (),
}


def project_dag() -> DagMap:
    return cast(DagMap, DagMap.new(_dag))
