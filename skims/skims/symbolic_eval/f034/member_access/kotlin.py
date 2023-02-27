from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def bytearray_as_seed(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    ma_attr = args.graph.nodes[args.n_id]
    args.evaluation[args.n_id] = ma_attr["member"] == "toByteArray"
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
