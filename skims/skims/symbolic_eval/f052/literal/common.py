from symbolic_eval.common import (
    INSECURE_ALGOS,
    INSECURE_MODES,
)
from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def insecure_create_cipher(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    if args.graph.nodes[args.n_id]["value_type"] == "string":
        cipher = args.graph.nodes[args.n_id]["value"][1:-1].lower().split("-")
        args.evaluation[args.n_id] = any(
            mode in cipher for mode in INSECURE_MODES
        ) or any(algo in cipher for algo in INSECURE_ALGOS)

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)


def insecure_sign_mechanism(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = bool(
        (args.graph.nodes[args.n_id].get("value_type") == "string")
        and (value := args.graph.nodes[args.n_id].get("value"))
        and (value.lower()[1:-1] in {"sha256", "sha1"})
    )

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
