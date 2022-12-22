from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def java_xpath_injection_evaluate(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    if args.graph.nodes[args.n_id]["variable_type"] == "HttpServletRequest":
        args.triggers.add("userconnection")
    if args.graph.nodes[args.n_id]["variable_type"] == "HttpServletResponse":
        args.triggers.add("userresponse")
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
