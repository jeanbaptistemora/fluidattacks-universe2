from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def python_unsafe_ldap(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    n_attrs = args.graph.nodes[args.n_id]
    expr = f'{n_attrs["expression"]}.{n_attrs["member"]}'
    if expr == "ldap.initialize":
        args.evaluation[args.n_id] = True
        args.triggers.add("ldapconnect")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
