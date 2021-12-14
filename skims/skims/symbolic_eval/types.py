from model.core_model import (
    FindingEnum,
)
from model.graph_model import (
    Graph,
    GraphShardMetadataLanguage as GraphLanguage,
    NId,
)
from typing import (
    Any,
    Callable,
    Dict,
    List,
    NamedTuple,
)

Path = List[NId]

SYMBOLIC_EVAL_ARGS = Any  # SymbolicEvalArgs


class SymbolicEvalArgs(NamedTuple):
    generic: Callable[[SYMBOLIC_EVAL_ARGS], bool]
    language: GraphLanguage
    finding: FindingEnum
    evaluation: Dict[NId, bool]
    graph: Graph
    path: Path
    n_id: NId

    def fork_n_id(self, n_id: NId) -> SYMBOLIC_EVAL_ARGS:
        return SymbolicEvalArgs(
            generic=self.generic,
            language=self.language,
            finding=self.finding,
            evaluation=self.evaluation,
            graph=self.graph,
            path=self.path,
            n_id=n_id,
        )

    def fork(self, **attrs: Any) -> SYMBOLIC_EVAL_ARGS:
        params = self._asdict()
        params.update(attrs)
        return SymbolicEvalArgs(**params)


Analyzer = Callable[[GraphLanguage, Graph], None]
LanguageAnalyzer = Callable[[Graph], None]
Evaluator = Callable[[SymbolicEvalArgs], bool]


class MissingSymbolicEval(Exception):
    pass


class BadMethodInvocation(Exception):
    pass
