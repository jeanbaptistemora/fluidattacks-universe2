from contextlib import (
    suppress,
)
from symbolic_eval.common import (
    INSECURE_HASHES,
)
from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)
from utils import (
    crypto,
)

SSL_SAFE_METHODS = {
    "tls",
    "tlsv1.2",
    "tlsv1.3",
    "dtls",
    "dtlsv1.2",
    "dtlsv1.3",
}


def kt_insecure_cipher(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    n_attrs = args.graph.nodes[args.n_id]
    if n_attrs["value_type"] == "string":
        key_value = n_attrs["value"][1:-1]
        alg, mode, pad, *_ = (key_value.lower() + "///").split("/", 3)
        args.evaluation[args.n_id] = crypto.is_vulnerable_cipher(
            alg, mode, pad
        )

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)


def kt_insecure_cipher_ssl(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    if args.graph.nodes[args.n_id]["value_type"] == "string":
        cipher_ssl = args.graph.nodes[args.n_id]["value"].replace('"', "")
        args.evaluation[args.n_id] = cipher_ssl.lower() not in SSL_SAFE_METHODS

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)


def kt_insecure_hash(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    if args.graph.nodes[args.n_id]["value_type"] == "string":
        member_str = args.graph.nodes[args.n_id]["value"]
        if member_str[1:-1].lower() in INSECURE_HASHES:
            args.evaluation[args.n_id] = True

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)


def kt_insecure_key(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    n_attrs = args.graph.nodes[args.n_id]
    if n_attrs["value_type"] == "number":
        key_value = n_attrs["value"]
        with suppress(TypeError):
            key_length = int(key_value)
            args.evaluation[args.n_id] = key_length < 2048

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)


def kt_insecure_key_ec(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    n_attrs = args.graph.nodes[args.n_id]
    if n_attrs["value_type"] == "string":
        key_value = n_attrs["value"][1:-1]
        args.evaluation[args.n_id] = crypto.insecure_elliptic_curve(key_value)

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)


def kt_insecure_key_gen(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    n_attrs = args.graph.nodes[args.n_id]
    if n_attrs["value_type"] == "number":
        key_value = n_attrs["value"]
        with suppress(TypeError):
            key_length = int(key_value)
            args.evaluation[args.n_id] = key_length < 128

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
