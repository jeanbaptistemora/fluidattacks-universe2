from model.core_model import (
    MethodsEnum,
)
from symbolic_eval.f052.pair.common import (
    insecure_key_pair,
    insecure_mode,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

METHOD_EVALUATORS: dict[MethodsEnum, Evaluator] = {
    MethodsEnum.JS_INSECURE_ENCRYPT: insecure_mode,
    MethodsEnum.TS_INSECURE_ENCRYPT: insecure_mode,
    MethodsEnum.JS_INSECURE_EC_KEYPAIR: insecure_key_pair,
    MethodsEnum.TS_INSECURE_EC_KEYPAIR: insecure_key_pair,
    MethodsEnum.JS_INSECURE_RSA_KEYPAIR: insecure_key_pair,
    MethodsEnum.TS_INSECURE_RSA_KEYPAIR: insecure_key_pair,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if language_evaluator := METHOD_EVALUATORS.get(args.method):
        return language_evaluator(args)
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
