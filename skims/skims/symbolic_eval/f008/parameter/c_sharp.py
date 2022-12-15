from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def cs_insec_addheader_write(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if args.graph.nodes[args.n_id]["variable_type"] == "HttpRequest":
        args.triggers.add("httpreq")
    if args.graph.nodes[args.n_id]["variable_type"] == "HttpResponse":
        args.triggers.add("httpres")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
