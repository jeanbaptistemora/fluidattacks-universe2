from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def cs_aes_secure_mode(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    unsafe_modes = {
        "CipherMode.ECB",
        "CipherMode.OFB",
        "CipherMode.CFB",
    }

    node = args.graph.nodes[args.n_id]
    if f'{node["expression"]}.{node["member"]}' in unsafe_modes:
        args.evaluation[args.n_id] = True

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
