from model.graph_model import (
    Graph,
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
    generic: Callable[[SYNTAX_CFG_ARGS], str]
    graph: Graph
    n_id: str
    nxt_id: Optional[str]

    def fork(self, n_id: str, nxt_id: Optional[str]) -> SYNTAX_CFG_ARGS:
        return SyntaxCfgArgs(
            generic=self.generic,
            graph=self.graph,
            n_id=n_id,
            nxt_id=nxt_id,
        )


CfgBuilder = Callable[[SyntaxCfgArgs], str]


class Dispatcher(NamedTuple):
    applicable_types: Set[str]
    cfg_builder: CfgBuilder


Dispatchers = Tuple[Dispatcher, ...]


class MissingCfgBuilder(Exception):
    pass
