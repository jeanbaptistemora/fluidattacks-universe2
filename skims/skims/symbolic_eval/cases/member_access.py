# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.core_model import (
    FindingEnum,
)
from symbolic_eval.f001.member_access import (
    evaluate as evaluate_member_access_f001,
)
from symbolic_eval.f004.member_access import (
    evaluate as evaluate_member_access_f004,
)
from symbolic_eval.f008.member_access import (
    evaluate as evaluate_member_access_f008,
)
from symbolic_eval.f016.member_access import (
    evaluate as evaluate_member_access_f016,
)
from symbolic_eval.f021.member_access import (
    evaluate as evaluate_member_access_f021,
)
from symbolic_eval.f052.member_access import (
    evaluate as evaluate_member_access_f052,
)
from symbolic_eval.f063.member_access import (
    evaluate as evaluate_member_access_f063,
)
from symbolic_eval.f085.member_access import (
    evaluate as evaluate_member_access_f085,
)
from symbolic_eval.f091.member_access import (
    evaluate as evaluate_member_access_f091,
)
from symbolic_eval.f096.member_access import (
    evaluate as evaluate_member_access_f096,
)
from symbolic_eval.f098.member_access import (
    evaluate as evaluate_member_access_f098,
)
from symbolic_eval.f107.member_access import (
    evaluate as evaluate_member_access_f107,
)
from symbolic_eval.f211.member_access import (
    evaluate as evaluate_member_access_f211,
)
from symbolic_eval.f239.member_access import (
    evaluate as evaluate_member_access_f239,
)
from symbolic_eval.f320.member_access import (
    evaluate as evaluate_member_access_f320,
)
from symbolic_eval.f413.member_access import (
    evaluate as evaluate_member_access_f413,
)
from symbolic_eval.f416.member_access import (
    evaluate as evaluate_member_access_f416,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)
from typing import (
    Dict,
)

FINDING_EVALUATORS: Dict[FindingEnum, Evaluator] = {
    FindingEnum.F001: evaluate_member_access_f001,
    FindingEnum.F004: evaluate_member_access_f004,
    FindingEnum.F008: evaluate_member_access_f008,
    FindingEnum.F016: evaluate_member_access_f016,
    FindingEnum.F021: evaluate_member_access_f021,
    FindingEnum.F052: evaluate_member_access_f052,
    FindingEnum.F085: evaluate_member_access_f085,
    FindingEnum.F091: evaluate_member_access_f091,
    FindingEnum.F096: evaluate_member_access_f096,
    FindingEnum.F063: evaluate_member_access_f063,
    FindingEnum.F098: evaluate_member_access_f098,
    FindingEnum.F107: evaluate_member_access_f107,
    FindingEnum.F211: evaluate_member_access_f211,
    FindingEnum.F239: evaluate_member_access_f239,
    FindingEnum.F320: evaluate_member_access_f320,
    FindingEnum.F413: evaluate_member_access_f413,
    FindingEnum.F416: evaluate_member_access_f416,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    expr_id = args.graph.nodes[args.n_id]["expression_id"]
    args.evaluation[args.n_id] = args.generic(args.fork_n_id(expr_id)).danger
    if finding_evaluator := FINDING_EVALUATORS.get(args.method.value.finding):
        args.evaluation[args.n_id] = finding_evaluator(args).danger

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
