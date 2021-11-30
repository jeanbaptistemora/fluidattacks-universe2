from model.graph_model import (
    Graph,
)
from symbolic_eval.context.search import (
    method_declaration,
    method_invocation,
    variable_declaration,
)
from symbolic_eval.context.search.types import (
    SearchArgs,
    Searcher,
    SearchResult,
)
from symbolic_eval.types import (
    Path,
)
from typing import (
    Dict,
    Iterator,
    Optional,
)

SEARCHERS: Dict[str, Searcher] = {
    "MethodDeclaration": method_declaration.search,
    "MethodInvocation": method_invocation.search,
    "VariableDeclaration": variable_declaration.search,
}


def search(
    graph: Graph, path: Path, symbol: str, def_only: bool
) -> Iterator[SearchResult]:
    for n_id in path:
        if searcher := SEARCHERS.get(graph.nodes[n_id]["label_type"]):
            yield from searcher(SearchArgs(graph, n_id, symbol, def_only))


def search_until_def(graph: Graph, path: Path, symbol: str) -> Iterator[str]:
    for is_def, ref_id in search(graph, path, symbol, def_only=False):
        yield ref_id
        if is_def:
            break


def definition_search(graph: Graph, path: Path, symbol: str) -> Optional[str]:
    for _, ref_id in search(graph, path, symbol, def_only=True):
        return ref_id
    return None
