from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

DANGER_METHODS = {
    "QueryString",
    "ReadLine",
    "GetString",
    "Cookies",
    "GetStream",
    "AcceptTcpClient",
}


def cs_sql_user_params(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    ma_attr = args.graph.nodes[args.n_id]

    if ma_attr["member"] in DANGER_METHODS or (
        "params.get" in f'{ma_attr["expression"]}.{ma_attr["member"]}'.lower()
    ):
        args.triggers.add("UserParams")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
