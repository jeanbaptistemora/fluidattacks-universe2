from symbolic_eval.common import (
    PYTHON_INPUTS,
)
from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def python_ldap_injection(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    n_attrs = args.graph.nodes[args.n_id]
    member_access = f'{n_attrs["expression"]}.{n_attrs["member"]}'
    if member_access in PYTHON_INPUTS:
        args.evaluation[args.n_id] = True
        args.triggers.add("userparams")
    elif member_access == "ldap.initialize":
        args.evaluation[args.n_id] = True
        args.triggers.add("ldapconnect")
    elif n_attrs["member"] in {"escape_filter_chars", "escape_dn_chars"}:
        args.triggers.add("sanitized")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
