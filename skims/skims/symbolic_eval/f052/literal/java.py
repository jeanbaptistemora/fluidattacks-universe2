# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from contextlib import (
    suppress,
)
from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)
from utils import (
    crypto,
)

INSECURE_HASHES = {"md2", "md4", "md5", "sha1", "sha-1"}


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


def java_insecure_key_secret(
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


def java_insecure_hash(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    if args.graph.nodes[args.n_id]["value_type"] == "string":
        member_str = args.graph.nodes[args.n_id]["value"]
        if member_str.lower().replace('"', "") in INSECURE_HASHES:
            args.evaluation[args.n_id] = True

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)


def java_insecure_cipher(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    if args.graph.nodes[args.n_id]["value_type"] == "string":
        member_str = args.graph.nodes[args.n_id]["value"].replace('"', "")
        args.triggers.add(member_str)

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
