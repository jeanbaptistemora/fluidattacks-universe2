# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

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
    "tlsv1.2",
    "tlsv1.3",
    "dtlsv1.2",
    "dtlsv1.3",
}


def java_insecure_hash(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    if args.graph.nodes[args.n_id]["value_type"] == "string":
        member_str = args.graph.nodes[args.n_id]["value"]
        if member_str.lower().replace('"', "") in INSECURE_HASHES:
            args.evaluation[args.n_id] = True

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)


def java_insecure_key_rsa(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    n_attrs = args.graph.nodes[args.n_id]
    if n_attrs["value_type"] == "number":
        key_value = n_attrs["value"].replace('"', "")
        with suppress(TypeError):
            key_length = int(key_value)
            args.evaluation[args.n_id] = key_length < 2048

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)


def java_insecure_key_ec(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    n_attrs = args.graph.nodes[args.n_id]
    if n_attrs["value_type"] == "string":
        key_value = n_attrs["value"].replace('"', "")
        args.evaluation[args.n_id] = crypto.insecure_elliptic_curve(key_value)

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)


def java_evaluate_cipher(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    n_attrs = args.graph.nodes[args.n_id]
    if n_attrs["value_type"] == "string":
        key_value = n_attrs["value"].replace('"', "")
        alg, mode, pad, *_ = (
            key_value.lower().replace('"', "") + "///"
        ).split("/", 3)
        args.evaluation[args.n_id] = crypto.is_vulnerable_cipher(
            alg, mode, pad
        )

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)


def java_insecure_cipher_ssl(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    if args.graph.nodes[args.n_id]["value_type"] == "string":
        cipher_ssl = args.graph.nodes[args.n_id]["value"].replace('"', "")
        args.evaluation[args.n_id] = cipher_ssl.lower() not in SSL_SAFE_METHODS

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)


def java_insecure_cipher_jmqi(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    n_attrs = args.graph.nodes[args.n_id]
    if n_attrs["value_type"] == "string":
        iana_cipher = n_attrs["value"].replace('"', "")
        args.evaluation[args.n_id] = crypto.is_iana_cipher_suite_vulnerable(
            iana_cipher
        )

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
