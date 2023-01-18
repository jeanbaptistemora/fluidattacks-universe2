from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def cs_regex_injection(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if args.graph.nodes[args.n_id]["variable_type"] == "HttpRequest":
        args.evaluation[args.n_id] = True
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)


def cs_vuln_regex(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if args.graph.nodes[args.n_id]["variable_type"] == "HttpRequest":
        args.triggers.add("userconnection")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
