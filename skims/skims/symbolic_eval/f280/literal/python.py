from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def xml_parser(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if args.graph.nodes[args.n_id]["value"][1:-1] == "sessionid":
        args.triggers.add("sessionid")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
