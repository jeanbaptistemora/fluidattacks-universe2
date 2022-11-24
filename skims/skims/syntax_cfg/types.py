from model.graph_model import (
    Graph,
    NId,
)
from typing import (
    Any,
    Callable,
    NamedTuple,
    Optional,
    Set,
    Tuple,
)

SYNTAX_CFG_ARGS = Any


class SyntaxCfgArgs(NamedTuple):
    generic: Callable[[SYNTAX_CFG_ARGS], NId]
    graph: Graph
    n_id: NId
    nxt_id: Optional[NId]

    def fork(self, n_id: NId, nxt_id: Optional[NId]) -> SYNTAX_CFG_ARGS:
        return SyntaxCfgArgs(
            generic=self.generic,
            graph=self.graph,
            n_id=n_id,
            nxt_id=nxt_id,
        )


CfgBuilder = Callable[[SyntaxCfgArgs], NId]


class Dispatcher(NamedTuple):
    applicable_types: Set[str]
    cfg_builder: CfgBuilder


Dispatchers = Tuple[Dispatcher, ...]


class MissingCfgBuilder(Exception):
    pass
