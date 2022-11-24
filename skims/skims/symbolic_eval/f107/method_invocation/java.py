from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def java_ldap_injection(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if args.graph.nodes[args.n_id]["expression"] == "getParameter":
        args.triggers.add("UserParams")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
