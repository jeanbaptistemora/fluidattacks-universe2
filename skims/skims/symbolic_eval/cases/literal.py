from model.core_model import (
    FindingEnum,
)
from symbolic_eval.f008.literal import (
    evaluate as evaluate_literal_f008,
)
from symbolic_eval.f012.literal import (
    evaluate as evaluate_literal_f012,
)
from symbolic_eval.f016.literal import (
    evaluate as evaluate_literal_f016,
)
from symbolic_eval.f017.literal import (
    evaluate as evaluate_literal_f017,
)
from symbolic_eval.f035.literal import (
    evaluate as evaluate_literal_f035,
)
from symbolic_eval.f042.literal import (
    evaluate as evaluate_literal_f042,
)
from symbolic_eval.f052.literal import (
    evaluate as evaluate_literal_f052,
)
from symbolic_eval.f060.literal import (
    evaluate as evaluate_literal_f060,
)
from symbolic_eval.f085.literal import (
    evaluate as evaluate_literal_f085,
)
from symbolic_eval.f091.literal import (
    evaluate as evaluate_literal_f091,
)
from symbolic_eval.f097.literal import (
    evaluate as evaluate_literal_f097,
)
from symbolic_eval.f134.literal import (
    evaluate as evaluate_literal_f134,
)
from symbolic_eval.f135.literal import (
    evaluate as evaluate_literal_f135,
)
from symbolic_eval.f152.literal import (
    evaluate as evaluate_literal_f152,
)
from symbolic_eval.f160.literal import (
    evaluate as evaluate_literal_f160,
)
from symbolic_eval.f211.literal import (
    evaluate as evaluate_literal_f211,
)
from symbolic_eval.f239.literal import (
    evaluate as evaluate_literal_f239,
)
from symbolic_eval.f309.literal import (
    evaluate as evaluate_literal_f309,
)
from symbolic_eval.f343.literal import (
    evaluate as evaluate_literal_f343,
)
from symbolic_eval.f354.literal import (
    evaluate as evaluate_literal_f354,
)
from symbolic_eval.f368.literal import (
    evaluate as evaluate_literal_f368,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)
from typing import (
    Dict,
)
from utils import (
    graph as g,
)

FINDING_EVALUATORS: Dict[FindingEnum, Evaluator] = {
    FindingEnum.F008: evaluate_literal_f008,
    FindingEnum.F012: evaluate_literal_f012,
    FindingEnum.F016: evaluate_literal_f016,
    FindingEnum.F017: evaluate_literal_f017,
    FindingEnum.F035: evaluate_literal_f035,
    FindingEnum.F042: evaluate_literal_f042,
    FindingEnum.F052: evaluate_literal_f052,
    FindingEnum.F060: evaluate_literal_f060,
    FindingEnum.F085: evaluate_literal_f085,
    FindingEnum.F091: evaluate_literal_f091,
    FindingEnum.F097: evaluate_literal_f097,
    FindingEnum.F134: evaluate_literal_f134,
    FindingEnum.F135: evaluate_literal_f135,
    FindingEnum.F152: evaluate_literal_f152,
    FindingEnum.F160: evaluate_literal_f160,
    FindingEnum.F211: evaluate_literal_f211,
    FindingEnum.F239: evaluate_literal_f239,
    FindingEnum.F309: evaluate_literal_f309,
    FindingEnum.F343: evaluate_literal_f343,
    FindingEnum.F354: evaluate_literal_f354,
    FindingEnum.F368: evaluate_literal_f368,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False

    s_ids = g.match_ast_group_d(args.graph, args.n_id, "SymbolLookup")
    if len(s_ids) > 0:
        danger = [args.generic(args.fork_n_id(_id)).danger for _id in s_ids]
        args.evaluation[args.n_id] = any(danger)

    if finding_evaluator := FINDING_EVALUATORS.get(args.method.value.finding):
        args.evaluation[args.n_id] = finding_evaluator(args).danger

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
