from collections.abc import (
    Callable,
)
from model.graph_model import (
    Graph,
    NId,
)
from typing import (
    Any,
    NamedTuple,
)

SYNTAX_CFG_ARGS = Any  # pylint: disable=invalid-name


class SyntaxCfgArgs(NamedTuple):
    generic: Callable[[SYNTAX_CFG_ARGS], NId]
    graph: Graph
    n_id: NId
    nxt_id: NId | None

    def fork(self, n_id: NId, nxt_id: NId | None) -> SYNTAX_CFG_ARGS:
        return SyntaxCfgArgs(
            generic=self.generic,
            graph=self.graph,
            n_id=n_id,
            nxt_id=nxt_id,
        )


CfgBuilder = Callable[[SyntaxCfgArgs], NId]


class Dispatcher(NamedTuple):
    applicable_types: set[str]
    cfg_builder: CfgBuilder


Dispatchers = tuple[Dispatcher, ...]


class MissingCfgBuilder(Exception):
    pass
