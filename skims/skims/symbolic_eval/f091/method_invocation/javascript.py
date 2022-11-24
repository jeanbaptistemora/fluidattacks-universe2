from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def javascript_insecure_logging(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    m_attr = args.graph.nodes[args.n_id]
    if "replace" in m_attr["expression"]:
        args.triggers.add("sanitized")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
