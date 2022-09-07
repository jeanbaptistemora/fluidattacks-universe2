# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from sast_symbolic_evaluation.types import (
    EvaluatorArgs,
)


def evaluate(args: EvaluatorArgs) -> None:
    args.syntax_step.meta.danger = any(
        dep.meta.danger for dep in args.dependencies
    )
    if len(args.dependencies) == 1:
        args.syntax_step.meta.value = args.dependencies[0].meta.value
