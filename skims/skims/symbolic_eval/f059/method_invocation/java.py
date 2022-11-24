from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def java_sensitive_logs_info(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    m_attr = args.graph.nodes[args.n_id]
    if (
        (obj_id := m_attr.get("object_id"))
        and (obj_name := args.graph.nodes[obj_id].get("symbol"))
        and f"{obj_name}.{m_attr['expression']}".lower() == "system.getenv"
    ):
        args.triggers.add("sensitiveinfo")
        args.evaluation[args.n_id] = True

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
