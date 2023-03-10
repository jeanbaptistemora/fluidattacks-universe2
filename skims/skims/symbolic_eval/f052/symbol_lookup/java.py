from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

DANGER_TLS = {
    "TlsVersion.TLS_1_0",
    "TlsVersion.TLS_1_1",
}


def java_insecure_connection(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if args.graph.nodes[args.n_id]["symbol"] in DANGER_TLS:
        args.evaluation[args.n_id] = True
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
