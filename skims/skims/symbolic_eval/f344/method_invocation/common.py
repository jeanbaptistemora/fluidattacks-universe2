from lib_root.utilities.javascript import (
    get_default_alias,
)
from model.graph_model import (
    Graph,
)
from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)
from typing import (
    Set,
)


def get_async_danger_imports(graph: Graph) -> Set[str]:
    danger_imports: Set[str] = {"fetch"}
    if axios_alias := get_default_alias(graph, "axios"):
        danger_imports.add(axios_alias)
    if ky_alias := get_default_alias(graph, "ky"):
        danger_imports.add(ky_alias)
    if ky_universal_alias := get_default_alias(graph, "ky-universal"):
        danger_imports.add(ky_universal_alias)
    return danger_imports


def js_ls_sensitive_data(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    nodes = args.graph.nodes[args.n_id]
    dangerous_imports: Set[str] = get_async_danger_imports(args.graph)
    args.evaluation[args.n_id] = nodes.get("expression") in dangerous_imports
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
