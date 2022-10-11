# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from symbolic_eval.context.search.types import (
    SearchArgs,
    SearchResult,
)
from symbolic_eval.context.utils import (
    build_ctx,
)
from typing import (
    Iterator,
)
from utils import (
    graph as g,
)

MODIFYING_METHODS = {"add", "push", "put"}


def search(args: SearchArgs) -> Iterator[SearchResult]:
    n_attr = args.graph.nodes[args.n_id]
    if not args.def_only:
        if (
            n_attr["expression"] in MODIFYING_METHODS
            and (obj_id := n_attr.get("object_id"))
            and args.symbol == args.graph.nodes[obj_id].get("symbol")
        ):
            yield False, args.n_id
        else:
            if "ctx_evaluated" not in args.graph.nodes[args.n_id]:
                build_ctx(args.graph, args.n_id, types={"SymbolLookup"})

            for c_id in g.adj_ctx(args.graph, args.n_id):
                if args.symbol == args.graph.nodes[c_id]["symbol"]:
                    yield False, c_id
