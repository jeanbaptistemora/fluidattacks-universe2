# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from symbolic_eval.types import (
    SymbolicEvalArgs,
)
from typing import (
    Set,
)

HTTP_INPUTS: Set[str] = {
    "Request.Params",
    "Request.Querystring",
    "Request.Form",
    "Request.Cookies",
    "Request.ServerVariables",
}

INSECURE_ALGOS = {
    "none",
    "blowfish",
    "bf",
    "des",
    "desede",
    "rc2",
    "rc4",
    "rsa",
}

INSECURE_MODES = {"ecb", "ofb", "cfb", "cbc"}

INSECURE_HASHES = {"md2", "md4", "md5", "sha1", "sha-1"}


def check_http_inputs(args: SymbolicEvalArgs) -> bool:
    ma_attr = args.graph.nodes[args.n_id]
    member_access = f'{ma_attr["expression"]}.{ma_attr["member"]}'
    return member_access in HTTP_INPUTS
