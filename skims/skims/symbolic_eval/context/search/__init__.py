from collections.abc import (
    Iterator,
)
from model.graph_model import (
    Graph,
    NId,
)
from symbolic_eval.context.search import (
    assignment,
    class_body,
    declaration_block,
    file_node,
    for_each,
    if_statement,
    method_declaration,
    method_invocation,
    using_statement,
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

SEARCHERS: dict[str, Searcher] = {
    "Assignment": assignment.search,
    "ClassBody": class_body.search,
    "DeclarationBlock": declaration_block.search,
    "File": file_node.search,
    "ForEachStatement": for_each.search,
    "If": if_statement.search,
    "MethodDeclaration": method_declaration.search,
    "MethodInvocation": method_invocation.search,
    "UsingStatement": using_statement.search,
    "VariableDeclaration": variable_declaration.search,
}


def search(
    graph: Graph, path: Path, symbol: str, def_only: bool
) -> Iterator[SearchResult]:
    for n_id in path:
        if searcher := SEARCHERS.get(graph.nodes[n_id]["label_type"]):
            yield from searcher(SearchArgs(graph, n_id, symbol, def_only))


def search_until_def(graph: Graph, path: Path, symbol: str) -> Iterator[NId]:
    for is_def, ref_id in search(graph, path, symbol, def_only=False):
        yield ref_id
        if is_def:
            break


def definition_search(graph: Graph, path: Path, symbol: str) -> NId | None:
    for _, ref_id in search(graph, path, symbol, def_only=True):
        return ref_id
    return None
