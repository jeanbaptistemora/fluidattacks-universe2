from model.graph_model import (
    Graph,
)
from symbolic_eval.search.cases import (
    method_declaration,
    parameter,
    parameter_list,
    variable_declaration,
)
from symbolic_eval.types import (
    Path,
    Searcher,
    SymbolicSearchArgs,
)
from typing import (
    Dict,
    Optional,
)

SEARCHERS: Dict[str, Searcher] = {
    "MethodDeclaration": method_declaration.search,
    "Parameter": parameter.search,
    "ParameterList": parameter_list.search,
    "VariableDeclaration": variable_declaration.search,
}


def generic(args: SymbolicSearchArgs) -> Optional[str]:
    node_type = args.graph.nodes[args.target_id]["label_type"]
    if searcher := SEARCHERS.get(node_type):
        return searcher(args)
    return None


def search(graph: Graph, target_id: str, symbol: str) -> Optional[str]:
    return generic(SymbolicSearchArgs(generic, graph, target_id, symbol))


def lookup_search(graph: Graph, path: Path, symbol: str) -> Optional[str]:
    if not path:
        return None

    target_id, *sub_path = path
    if reference_id := search(graph, target_id, symbol):
        return reference_id
    return lookup_search(graph, sub_path, symbol)
