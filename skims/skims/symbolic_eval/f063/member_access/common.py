from symbolic_eval.common import (
    check_js_ts_http_inputs,
)
from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def insecure_path_traversal(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if check_js_ts_http_inputs(args):
        args.evaluation[args.n_id] = True
    if args.graph.nodes[args.n_id]["expression"] == "resolve":
        args.triggers.add("resolve")
    if args.graph.nodes[args.n_id]["expression"].lower() == "startswith":
        args.triggers.add("sanitize")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)


def zip_slip(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if args.graph.nodes[args.n_id]["expression"] == "entryName":
        args.evaluation[args.n_id] = True
    if args.graph.nodes[args.n_id]["expression"] == "join":
        args.triggers.add("resolve")
    if args.graph.nodes[args.n_id]["expression"].lower() == "startswith":
        args.triggers.add("sanitize")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
