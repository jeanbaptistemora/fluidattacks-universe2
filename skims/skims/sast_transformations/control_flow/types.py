from model.graph_model import (
    Graph,
)
from mypy_extensions import (
    NamedArg,
)
from typing import (
    Callable,
    Dict,
    List,
    NamedTuple,
    Set,
)

EdgeAttrs = Dict[str, str]
Frame = Dict[str, str]  # {type: node_type, next_id: n_id}
Stack = List[Frame]
GenericType = Callable[
    [
        Graph,
        str,
        Stack,
        NamedArg(EdgeAttrs, "edge_attrs"),  # noqa
    ],
    None,
]


class Walker(NamedTuple):
    applicable_node_label_types: Set[str]
    walk_fun: Callable[[Graph, str, Stack, GenericType], None]
