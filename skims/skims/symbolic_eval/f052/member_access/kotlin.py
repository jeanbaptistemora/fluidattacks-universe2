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


def kt_insecure_init_vector(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    graph = args.graph
    n_attrs = args.graph.nodes[args.n_id]
    if (
        n_attrs["member"] == "toByteArray"
        and (val := n_attrs["expression_id"])
        and graph.nodes[val]["label_type"] == "Literal"
        and graph.nodes[val]["value_type"] == "string"
    ):
        args.evaluation[args.n_id] = True

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
