from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def cs_vuln_regex(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    value = args.graph.nodes[args.n_id]["value"]
    # Other insecure regex patterns must be added here
    insecure_chars = (".*", ")*", "+)", "+.)", ")+", "/g", r"\s")
    if any(c in value for c in insecure_chars):
        args.evaluation[args.n_id] = True

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
