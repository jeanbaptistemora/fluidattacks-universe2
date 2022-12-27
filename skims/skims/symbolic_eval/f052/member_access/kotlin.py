from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

INSECURE_CIPHERS = {
    "tlsversion.ssl_3_0",
    "tlsversion.tls_1_0",
    "tlsversion.tls_1_1",
}


def kt_insecure_cipher_http(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    n_attrs = args.graph.nodes[args.n_id]
    if (
        f'{n_attrs["expression"]}.{n_attrs["member"]}'.lower()
        in INSECURE_CIPHERS
    ):
        args.evaluation[args.n_id] = True

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
