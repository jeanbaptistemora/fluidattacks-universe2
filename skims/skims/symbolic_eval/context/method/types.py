from collections.abc import (
    Callable,
)
from model.graph_model import (
    Graph,
    NId,
)
from symbolic_eval.types import (
    Path,
)
from typing import (
    Any,
    NamedTuple,
)

SOLVER_ARGS = Any  # pylint: disable=invalid-name


class SolverArgs(NamedTuple):
    generic: Callable[[SOLVER_ARGS], NId | None]
    graph: Graph
    path: Path
    n_id: NId

    def fork_n_id(self, n_id: NId) -> SOLVER_ARGS:
        return SolverArgs(
            generic=self.generic,
            graph=self.graph,
            path=self.path,
            n_id=n_id,
        )


Solver = Callable[[SolverArgs], NId | None]
