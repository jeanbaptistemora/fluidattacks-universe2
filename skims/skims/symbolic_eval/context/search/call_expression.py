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
    if args.symbol in args.graph.nodes[args.n_id]["function_name"].split("."):
        yield True, args.n_id
