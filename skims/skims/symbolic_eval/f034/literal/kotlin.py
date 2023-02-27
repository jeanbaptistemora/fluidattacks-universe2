from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def seed_hardcoded(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = True
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
