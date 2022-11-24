from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def cs_insec_access_protocol(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    ma_attr = args.graph.nodes[args.n_id]
    args.evaluation[args.n_id] = (
        ma_attr["expression"] == "SharedAccessProtocol"
        and ma_attr["member"] == "HttpsOrHttp"
    )
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
