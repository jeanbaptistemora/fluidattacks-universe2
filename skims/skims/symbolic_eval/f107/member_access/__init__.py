from model.core_model import (
    MethodsEnum,
)
from symbolic_eval.f107.member_access.c_sharp import (
    cs_ldap_injection,
)
from symbolic_eval.f107.member_access.python import (
    python_ldap_injection,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

METHOD_EVALUATORS: dict[MethodsEnum, Evaluator] = {
    MethodsEnum.CS_LDAP_INJECTION: cs_ldap_injection,
    MethodsEnum.PYTHON_LDAP_INJECTION: python_ldap_injection,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if language_evaluator := METHOD_EVALUATORS.get(args.method):
        return language_evaluator(args)
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
