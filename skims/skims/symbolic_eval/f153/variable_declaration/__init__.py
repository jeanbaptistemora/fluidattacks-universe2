from model.core_model import (
    MethodsEnum,
)
from symbolic_eval.f153.variable_declaration.java import (
    allow_all_mime_types as java_allows_all_mime_types,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

METHOD_EVALUATORS: dict[MethodsEnum, Evaluator] = {
    MethodsEnum.JAVA_HTTP_REQ_ACCEPTS_ANY_MYMETYPE: java_allows_all_mime_types,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if language_evaluator := METHOD_EVALUATORS.get(args.method):
        return language_evaluator(args)
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
