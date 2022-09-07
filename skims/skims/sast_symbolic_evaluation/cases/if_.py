# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from sast_symbolic_evaluation.types import (
    EvaluatorArgs,
    ImpossiblePath,
)


def evaluate(args: EvaluatorArgs) -> None:
    (predicate,) = args.dependencies

    if args.n_id_next and (
        (
            predicate.meta.value is True
            and args.n_id_next != args.syntax_step.n_id_true
        )
        or (
            predicate.meta.value is False
            and args.n_id_next != args.syntax_step.n_id_false
        )
    ):
        # We are walking a path that should not happen
        raise ImpossiblePath()
