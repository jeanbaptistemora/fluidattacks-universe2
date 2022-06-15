from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def symb_insec_create(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    ma_attr = args.graph.nodes[args.n_id]
    member_access = f'{ma_attr["expression"]}.{ma_attr["member"]}'
    args.evaluation[args.n_id] = member_access == "WebRequest.Create"
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
