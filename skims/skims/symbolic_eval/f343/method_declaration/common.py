from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def js_insecure_compression(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    args.triggers.add("custom_function")
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
