from model.graph_model import (
    Graph,
)
from typing import (
    Any,
    Callable,
    Dict,
    List,
    NamedTuple,
    Set,
)

EdgeAttrs = Dict[str, str]
Frame = Any  # will add types once I discover the pattern
Stack = List[Frame]


class Walker(NamedTuple):
    applicable_node_label_types: Set[str]
    walk_fun: Callable[[Graph, str, Stack], None]
