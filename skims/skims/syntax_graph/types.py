from model.graph_model import (
    Graph,
    GraphShardMetadataLanguage as GraphLanguage,
    NId,
)
from typing import (
    Any,
    Callable,
    NamedTuple,
    Set,
    Tuple,
)

SYNTAX_GRAPH_ARGS = Any


class SyntaxGraphArgs(NamedTuple):
    generic: Callable[[SYNTAX_GRAPH_ARGS], NId]
    language: GraphLanguage
    ast_graph: Graph
    syntax_graph: Graph
    n_id: NId

    def fork_n_id(self, n_id: NId) -> SYNTAX_GRAPH_ARGS:
        return SyntaxGraphArgs(
            generic=self.generic,
            language=self.language,
            ast_graph=self.ast_graph,
            syntax_graph=self.syntax_graph,
            n_id=n_id,
        )


SyntaxReader = Callable[[SyntaxGraphArgs], NId]


class Dispatcher(NamedTuple):
    applicable_types: Set[str]
    syntax_reader: SyntaxReader


Dispatchers = Tuple[Dispatcher, ...]


class MissingSyntaxReader(Exception):
    pass


class MissingCaseHandling(Exception):
    pass
