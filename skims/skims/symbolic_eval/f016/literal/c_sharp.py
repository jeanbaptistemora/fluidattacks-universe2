from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def cs_service_point_disabled(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    member_str = (
        "Switch.System.ServiceModel."
        + "DisableUsingServicePointManagerSecurityProtocols"
    )

    if args.graph.nodes[args.n_id]["value"] == '"' + member_str + '"':
        args.evaluation[args.n_id] = True
        args.triggers.add(member_str)
    if args.graph.nodes[args.n_id]["value"] == "true":
        args.evaluation[args.n_id] = True
        args.triggers.add("true")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
