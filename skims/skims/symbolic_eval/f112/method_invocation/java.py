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

SQL_CONNECTIONS = {"getSqlStatement", "getSqlConnection"}


def java_sql_injection(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    ma_attr = args.graph.nodes[args.n_id]
    if ma_attr["expression"] in DANGER_METHODS:
        args.triggers.add("userparameters")
    elif ma_attr["expression"] in SQL_CONNECTIONS:
        args.evaluation[args.n_id] = True

    if ma_attr["expression"] == "get" and (obj_id := ma_attr.get("object_id")):
        expr_eval = args.generic(args.fork(n_id=obj_id))
        if expr_eval and expr_eval.danger:
            args.evaluation[args.n_id] = True
            args.triggers.add("userparameters")

    if ma_attr["expression"] == "replaceAll":
        args.triggers.add("sanitize")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
