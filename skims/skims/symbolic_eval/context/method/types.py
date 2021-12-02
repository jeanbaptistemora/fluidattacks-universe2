from model.graph_model import (
    Graph,
)
from symbolic_eval.types import (
    Path,
)
from typing import (
    Any,
    Callable,
    NamedTuple,
    Optional,
)

SOLVER_ARGS = Any  # SymbolicEvalArgs


class SolverArgs(NamedTuple):
    generic: Callable[[SOLVER_ARGS], Optional[str]]
    graph: Graph
    path: Path
    n_id: str

    def fork_n_id(self, n_id: str) -> SOLVER_ARGS:
        return SolverArgs(
            generic=self.generic,
            graph=self.graph,
            path=self.path,
            n_id=n_id,
        )


Solver = Callable[[SolverArgs], Optional[str]]
