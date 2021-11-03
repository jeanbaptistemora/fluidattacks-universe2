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
)

Path = List[str]

SYMBOLIC_EVAL_ARGS = Any  # SymbolicEvalArgs


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


Analyzer = Callable[[GraphLanguage, Graph], None]
LanguageAnalyzer = Callable[[Graph], None]
Evaluator = Callable[[SymbolicEvalArgs], bool]


class MissingSymbolicEval(Exception):
    pass
