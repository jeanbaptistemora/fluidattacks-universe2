from model.core_model import (
    FindingEnum,
)
from model.graph_model import (
    Graph,
    GraphShardMetadataLanguage as GraphLanguage,
)
from typing import (
    Any,
    Callable,
    List,
    NamedTuple,
    Optional,
)

Path = List[str]

SYMBOLIC_EVAL_ARGS = Any  # SymbolicEvalArgs
SYMBOLIC_SEARCH_ARGS = Any  # SymbolicSearchArgs


class SymbolicEvalArgs(NamedTuple):
    generic: Callable[[SYMBOLIC_EVAL_ARGS], bool]
    language: GraphLanguage
    finding: FindingEnum
    graph: Graph
    path: Path
    n_id: str

    def fork_n_id(self, n_id: str) -> SYMBOLIC_EVAL_ARGS:
        return SymbolicEvalArgs(
            generic=self.generic,
            language=self.language,
            finding=self.finding,
            graph=self.graph,
            path=self.path,
            n_id=n_id,
        )


class SymbolicSearchArgs(NamedTuple):
    generic: Callable[[SYMBOLIC_SEARCH_ARGS], Optional[str]]
    graph: Graph
    target_id: str
    symbol: str

    def fork_target_id(self, target_id: str) -> SYMBOLIC_SEARCH_ARGS:
        return SymbolicSearchArgs(
            generic=self.generic,
            graph=self.graph,
            target_id=target_id,
            symbol=self.symbol,
        )


Analyzer = Callable[[GraphLanguage, Graph], None]
LanguageAnalyzer = Callable[[Graph], None]
Evaluator = Callable[[SymbolicEvalArgs], bool]
Searcher = Callable[[SymbolicSearchArgs], Optional[str]]


class MissingSymbolicEval(Exception):
    pass
