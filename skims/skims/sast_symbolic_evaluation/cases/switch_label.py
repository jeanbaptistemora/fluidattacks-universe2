# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model import (
    graph_model,
)
from sast_symbolic_evaluation.types import (
    EvaluatorArgs,
    ImpossiblePath,
)


def evaluate(args: EvaluatorArgs) -> None:
    pred, *cases = args.dependencies

    # We don't know the value of the predicate so let's stop here
    if pred.meta.value is None:
        return

    switch_n_id_next = None

    # Follow every `case X:` in search of the next_id
    for case in cases:
        if (
            isinstance(case, graph_model.SyntaxStepSwitchLabelCase)
            and case.meta.value == pred.meta.value
        ):
            switch_n_id_next = case.meta.n_id
            break

    # Follow every `default:` in search of the next_id
    if switch_n_id_next is None:
        for case in cases:
            if isinstance(case, graph_model.SyntaxStepSwitchLabelDefault):
                switch_n_id_next = case.meta.n_id
                break

    if switch_n_id_next is not None and args.n_id_next != switch_n_id_next:
        # We are walking a path that should not happen
        raise ImpossiblePath()
