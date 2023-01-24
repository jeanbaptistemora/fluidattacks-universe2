from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def js_ls_sensitive_data(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if method_name := args.graph.nodes[args.n_id].get("expression"):
        args.triggers.add(method_name)
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
