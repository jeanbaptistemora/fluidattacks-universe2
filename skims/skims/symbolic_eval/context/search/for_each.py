# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from symbolic_eval.context.search.types import (
    SearchArgs,
    SearchResult,
)
from typing import (
    Iterator,
)


def search(args: SearchArgs) -> Iterator[SearchResult]:
    variable_id = args.graph.nodes[args.n_id]["variable_id"]
    if args.symbol == args.graph.nodes[variable_id].get("symbol"):
        yield True, args.n_id
