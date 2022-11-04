# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from symbolic_eval.context.method.types import (
    SolverArgs,
)
from symbolic_eval.context.search import (
    definition_search,
)
from symbolic_eval.utils import (
    get_lookup_path,
)
from typing import (
    Optional,
)


def solve(args: SolverArgs) -> Optional[NId]:
    symbol = args.graph.nodes[args.n_id]["symbol"]
    try:
        search_path = get_lookup_path(args.graph, args.path, args.n_id)
    except ValueError:
        return None

    return definition_search(args.graph, search_path, symbol)
