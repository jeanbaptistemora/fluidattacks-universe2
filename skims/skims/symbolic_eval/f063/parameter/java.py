from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def java_zip_slip_injection(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if args.graph.nodes[args.n_id]["variable_type"] == "ZipFile":
        args.triggers.add("ZipFile")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
