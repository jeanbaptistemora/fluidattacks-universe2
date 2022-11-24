from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)
from symbolic_eval.utils import (
    get_object_identifiers,
    get_value_member_access,
)


def cs_httpclient_revocation_lst(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    if args.graph.nodes[args.n_id].get("name") == "WinHttpHandler":
        for ident in get_object_identifiers(args.graph, {"WinHttpHandler"}):
            if (
                member_val := get_value_member_access(
                    args.graph, ident, "CheckCertificateRevocationList"
                )
            ) and args.graph.nodes[member_val].get("value") == "false":
                args.evaluation[args.n_id] = True
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
