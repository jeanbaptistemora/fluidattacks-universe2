from model.graph_model import (
    Graph,
    GraphShardMetadataLanguage,
)
from typing import (
    Any,
    Callable,
    Dict,
    List,
    NamedTuple,
)

Frame = Dict[str, str]  # {type: node_type, next_id: n_id}
Stack = List[Frame]


CFG_ARGS = Any  # pylint: disable=invalid-name


class CfgArgs(NamedTuple):
    generic: Callable[[CFG_ARGS, Stack], None]
    graph: Graph
    n_id: str
    language: GraphShardMetadataLanguage

    def fork_n_id(self, n_id: str) -> CFG_ARGS:
        return CfgArgs(
            generic=self.generic,
            graph=self.graph,
            n_id=n_id,
            language=self.language,
        )


CfgBuilder = Callable[[CfgArgs, Stack], None]
