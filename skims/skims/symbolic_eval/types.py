from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
    Vulnerability,
)
from model.graph_model import (
    Graph,
    GraphShard,
    NId,
)
from typing import (
    Any,
    Callable,
    Dict,
    Iterator,
    List,
    NamedTuple,
    Set,
)
from xmlrpc.client import (
    boolean,
)

Path = List[NId]

SYMBOLIC_EVAL_ARGS = Any  # pylint: disable=invalid-name


class SymbolicEvaluation(NamedTuple):
    danger: boolean
    triggers: Set[str]


class SymbolicEvalArgs(NamedTuple):
    generic: Callable[[SYMBOLIC_EVAL_ARGS], SymbolicEvaluation]
    method: MethodsEnum
    evaluation: Dict[NId, bool]
    graph: Graph
    path: Path
    n_id: NId
    triggers: Set[str]

    def fork_n_id(self, n_id: NId) -> SYMBOLIC_EVAL_ARGS:
        return SymbolicEvalArgs(
            generic=self.generic,
            method=self.method,
            evaluation=self.evaluation,
            triggers=self.triggers,
            graph=self.graph,
            path=self.path,
            n_id=n_id,
        )

    def fork(self, **attrs: Any) -> SYMBOLIC_EVAL_ARGS:
        params = self._asdict()
        params.update(attrs)
        return SymbolicEvalArgs(**params)


Analyzer = Callable[[GraphShard], Vulnerabilities]
LanguageAnalyzer = Callable[[GraphShard], Iterator[Vulnerability]]
Evaluator = Callable[[SymbolicEvalArgs], SymbolicEvaluation]


class MissingSymbolicEval(Exception):
    pass


class BadMethodInvocation(Exception):
    pass


class MissingAnalizer(Exception):
    pass


class MissingLanguageAnalizer(Exception):
    pass
