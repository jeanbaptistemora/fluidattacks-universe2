# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from symbolic_eval.common import (
    INSECURE_MODES,
)
from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def cs_managed_secure_mode(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    n_attrs = args.graph.nodes[args.n_id]
    if n_attrs["member"].lower() in INSECURE_MODES:
        args.evaluation[args.n_id] = True

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
