from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def symb_insec_addheader_write(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if args.graph.nodes[args.n_id]["variable_type"] == "HttpRequest":
        args.evaluation[args.n_id] = True

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
