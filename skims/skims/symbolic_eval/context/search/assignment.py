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
from utils import (
    graph as g,
)


def search(args: SearchArgs) -> Iterator[SearchResult]:
    assign_id = g.adj_ast(args.graph, args.n_id)[0]
    if args.symbol == args.graph.nodes[assign_id].get("symbol"):
        yield True, args.n_id
    elif args.graph.nodes[assign_id]["label_type"] == "NewExpression":
        arg_id = args.graph.nodes[assign_id]["arguments_id"]
        value = args.graph.nodes[arg_id]["value"].replace('"', "")
        if value == args.symbol:
            yield True, args.n_id
