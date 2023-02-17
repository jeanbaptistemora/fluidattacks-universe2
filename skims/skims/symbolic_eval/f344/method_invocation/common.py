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
from utils import (
    graph as g,
)


def get_async_danger_imports(graph: Graph) -> set[str]:
    danger_imports: set[str] = {"fetch"}
    if axios_alias := get_default_alias(graph, "axios"):
        danger_imports.add(axios_alias)
    if ky_alias := get_default_alias(graph, "ky"):
        danger_imports.add(ky_alias)
    if ky_universal_alias := get_default_alias(graph, "ky-universal"):
        danger_imports.add(ky_universal_alias)
    return danger_imports


def js_ls_sensitive_data(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    node = args.graph.nodes[args.n_id]
    dangerous_imports: set[str] = get_async_danger_imports(args.graph)
    if (
        (method_expression := node.get("expression"))
        and (method_name := method_expression.split(".")[0])
        and (method_name in dangerous_imports)
    ):
        args.evaluation[args.n_id] = True
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)


def js_ls_sens_data_this(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    nodes = args.graph.nodes
    if (
        nodes[args.n_id].get("expression") == "localStorage.setItem"
        and (
            suspicious_n_ids := g.get_nodes_by_path(
                args.graph, args.n_id, [], "ArgumentList", "MemberAccess"
            )
        )
        and (suspicious_n_id := next(iter(suspicious_n_ids), None))
        and (nodes[suspicious_n_id].get("member") == "this")
    ):
        args.triggers.add(f"this_{suspicious_n_id}")
        args.evaluation[args.n_id] = True
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
