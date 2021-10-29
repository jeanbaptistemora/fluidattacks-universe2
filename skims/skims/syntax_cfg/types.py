from model.graph_model import (
    Graph,
)
from typing import (
    Any,
    Callable,
    List,
    NamedTuple,
    Set,
    Tuple,
)

Stack = List[str]
SYNTAX_CFG_ARGS = Any


class SyntaxCfgArgs(NamedTuple):
    generic: Callable[[SYNTAX_CFG_ARGS, Stack], None]
    graph: Graph
    n_id: str

    def fork_n_id(self, n_id: str) -> SYNTAX_CFG_ARGS:
        return SyntaxCfgArgs(
            generic=self.generic,
            graph=self.graph,
            n_id=n_id,
        )


CfgBuilder = Callable[[SyntaxCfgArgs, Stack], None]


class Dispatcher(NamedTuple):
    applicable_types: Set[str]
    cfg_builder: CfgBuilder


Dispatchers = Tuple[Dispatcher, ...]


class MissingCfgBuilder(Exception):
    pass
