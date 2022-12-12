from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def java_vuln_regex(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    value = args.graph.nodes[args.n_id]["value"]
    # Other insecure regex patterns must be added here
    insecure_chars = ("(.*", "+)*", "+.)", "+)+", "+)?", "?)+")
    if any(char in value for char in insecure_chars):
        args.evaluation[args.n_id] = True

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
