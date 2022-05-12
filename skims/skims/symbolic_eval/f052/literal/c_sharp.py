from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if (
        args.graph.nodes[args.n_id]["value"]
        == '"Switch.System.Net.DontEnableSchUseStrongCrypto"'
    ):
        args.evaluation[args.n_id] = True
        args.triggers.add("Switch.System.Net.DontEnableSchUseStrongCrypto")
    if args.graph.nodes[args.n_id]["value"] == "true":
        args.evaluation[args.n_id] = True
        args.triggers.add("true")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
