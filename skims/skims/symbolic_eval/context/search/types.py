# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    Graph,
    NId,
)
from typing import (
    Callable,
    Iterator,
    NamedTuple,
    Tuple,
)

# Bool value indicates whether the founded node is a definition or not
SearchResult = Tuple[bool, NId]


class SearchArgs(NamedTuple):
    graph: Graph
    n_id: NId
    symbol: str
    def_only: bool


Searcher = Callable[[SearchArgs], Iterator[SearchResult]]
