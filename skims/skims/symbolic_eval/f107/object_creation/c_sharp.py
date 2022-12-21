from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

DANGER_OBJ = {"StreamReader", "SqlCommand"}


def cs_ldap_injection(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if args.graph.nodes[args.n_id]["name"] in DANGER_OBJ:
        args.triggers.add("userconnection")
    if args.graph.nodes[args.n_id]["name"] == "DirectorySearcher":
        args.triggers.add("directorysearcher")
        args.evaluation[args.n_id] = True

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
