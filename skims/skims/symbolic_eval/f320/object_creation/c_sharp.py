from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def cs_ldap_auth(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    if args.graph.nodes[args.n_id]["name"] == "DirectoryEntry":
        args.triggers.add("VulnObject")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
