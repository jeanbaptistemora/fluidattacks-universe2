from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)
from utils import (
    string,
)


def java_trust_boundary_violation(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    lib = string.build_attr_paths(
        "javax", "servlet", "http", "HttpServletRequest"
    )

    if args.graph.nodes[args.n_id]["variable_type"] in lib:
        args.triggers.add("userconnection")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
