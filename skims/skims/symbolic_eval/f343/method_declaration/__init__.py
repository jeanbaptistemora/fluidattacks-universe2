from model.core_model import (
    MethodsEnum,
)
from symbolic_eval.f343.method_declaration.common import (
    js_insecure_compression,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

METHOD_EVALUATORS: dict[MethodsEnum, Evaluator] = {
    MethodsEnum.JS_INSECURE_COMPRESSION_ALGORITHM: js_insecure_compression,
    MethodsEnum.TS_INSECURE_COMPRESSION_ALGORITHM: js_insecure_compression,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if language_evaluator := METHOD_EVALUATORS.get(args.method):
        return language_evaluator(args)
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
