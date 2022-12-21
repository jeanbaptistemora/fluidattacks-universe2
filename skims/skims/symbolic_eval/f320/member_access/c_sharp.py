from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def cs_ldap_authenticated(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    insecure_types = {"None", "Anonymous"}
    if args.graph.nodes[args.n_id]["member"] in insecure_types:
        args.triggers.add("VulnAssignement")
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
