from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def xml_parser(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    ma_attr = args.graph.nodes[args.n_id]["expression"]
    if ma_attr == "HttpResponse":
        args.evaluation[args.n_id] = True
        args.triggers.add("httpresponse")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
