from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def java_vuln_regex(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    values = args.graph.nodes[args.n_id]["variable_type"].split(".")
    if values[-1] == "HttpServletRequest":
        args.triggers.add("HttpParams")
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
