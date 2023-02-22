from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def insecure_sign_async(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    nodes = args.graph.nodes
    if (
        (nodes[args.n_id].get("variable") == "alg")
        and (val_n_id := nodes[args.n_id].get("value_id"))
        and (nodes[val_n_id].get("label_type") == "Literal")
        and (nodes[val_n_id].get("value").lower()[1:-1] == "hs256")
    ):
        args.evaluation[args.n_id] = True
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
