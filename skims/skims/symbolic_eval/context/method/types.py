# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    Graph,
    NId,
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
    generic: Callable[[SOLVER_ARGS], Optional[NId]]
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


Solver = Callable[[SolverArgs], Optional[NId]]
