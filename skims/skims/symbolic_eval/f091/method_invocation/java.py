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


def java_insecure_logging(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    m_attr = args.graph.nodes[args.n_id]
    if m_attr["expression"] == "replaceAll":
        args.triggers.add("sanitized")

    if m_attr["expression"] in DANGER_METHODS:
        args.triggers.add("userparams")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
