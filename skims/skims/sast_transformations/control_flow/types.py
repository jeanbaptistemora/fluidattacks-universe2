from model.graph_model import (
    Graph,
    GraphShardMetadataLanguage,
)
from mypy_extensions import (
    NamedArg,
)
from typing import (
    Any,
    Callable,
    Dict,
    List,
    NamedTuple,
    Set,
    Tuple,
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


CFG_ARGS = Any


class CfgArgs(NamedTuple):
    generic: Callable[[CFG_ARGS, Stack], None]
    graph: Graph
    n_id: str
    language: GraphShardMetadataLanguage
    edge_attrs: EdgeAttrs

    def fork_n_id(self, n_id: str) -> CFG_ARGS:
        return CfgArgs(
            generic=self.generic,
            graph=self.graph,
            n_id=n_id,
            language=self.language,
            edge_attrs=self.edge_attrs,
        )


CfgBuilder = Callable[[CfgArgs, Stack], None]


class Walker(NamedTuple):
    applicable_node_label_types: Set[str]
    walk_fun: Callable[[Graph, str, Stack, GenericType], None]


Walkers = Tuple[Walker, ...]
