from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def dart_uses_logger_method(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    m_attr = args.graph.nodes[args.n_id]
    if "Logger" in m_attr["expression"]:
        args.triggers.add("usesLogger")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
