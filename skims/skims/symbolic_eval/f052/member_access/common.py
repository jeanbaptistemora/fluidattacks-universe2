from symbolic_eval.common import (
    INSECURE_MODES,
)
from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def insecure_mode(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    node = args.graph.nodes[args.n_id]
    if (
        node["member"].split(".")[-1].lower() in {"mode", "ciphermode"}
        and node["expression"].lower() in INSECURE_MODES
    ):
        args.evaluation[args.n_id] = True

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
