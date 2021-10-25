from model.graph_model import (
    Graph,
    GraphShardMetadataLanguage as GraphLanguage,
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
    generic: Callable[[SYNTAX_GRAPH_ARGS], str]
    language: GraphLanguage
    ast_graph: Graph
    syntax_graph: Graph
    n_id: str

    def fork_n_id(self, n_id: str) -> SYNTAX_GRAPH_ARGS:
        return SyntaxGraphArgs(
            generic=self.generic,
            language=self.language,
            ast_graph=self.ast_graph,
            syntax_graph=self.syntax_graph,
            n_id=n_id,
        )


SyntaxReader = Callable[[SyntaxGraphArgs], str]


class Dispatcher(NamedTuple):
    applicable_types: Set[str]
    syntax_reader: SyntaxReader


Dispatchers = Tuple[Dispatcher, ...]


class MissingSyntaxReader(Exception):
    pass
