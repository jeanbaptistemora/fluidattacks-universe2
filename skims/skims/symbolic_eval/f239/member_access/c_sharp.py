from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def cs_info_leak_errors(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    ma_attr = args.graph.nodes[args.n_id]
    member_access = f'{ma_attr["expression"]}.{ma_attr["member"]}'
    args.evaluation[args.n_id] = (
        member_access == "WebHostDefaults.DetailedErrorsKey"
    )
    if args.evaluation[args.n_id]:
        args.triggers.add("WebHostDefaults.DetailedErrorsKey")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
