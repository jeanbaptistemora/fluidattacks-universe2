from model.graph_model import (
    Graph,
)
from typing import (
    Callable,
    Iterator,
    NamedTuple,
    Tuple,
)

# Bool value indicates whether the founded node is a definition or not
SearchResult = Tuple[bool, str]


class SearchArgs(NamedTuple):
    graph: Graph
    n_id: str
    symbol: str
    def_only: bool


Searcher = Callable[[SearchArgs], Iterator[SearchResult]]
