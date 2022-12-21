from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

DANGER_METHODS = {
    "getBytes",
    "getHeader",
    "getHeaderNames",
    "getHeaders",
    "getName",
    "getParameter",
    "getParameterMap",
    "getParameterNames",
    "getParameterValues",
    "getQueryString",
    "getValue",
}


def java_ldap_injection(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    ma_attr = args.graph.nodes[args.n_id]
    if ma_attr["expression"] in DANGER_METHODS:
        args.evaluation[args.n_id] = True
        args.triggers.add("userparameters")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
