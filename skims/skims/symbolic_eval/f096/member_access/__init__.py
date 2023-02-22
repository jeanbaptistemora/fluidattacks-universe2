from model.core_model import (
    MethodsEnum,
)
from symbolic_eval.f096.member_access.c_sharp import (
    cs_type_name_handling,
    cs_xml_serial,
)
from symbolic_eval.f096.member_access.python import (
    deserialization_injection,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

METHOD_EVALUATORS: dict[MethodsEnum, Evaluator] = {
    MethodsEnum.CS_TYPE_NAME_HANDLING: cs_type_name_handling,
    MethodsEnum.CS_XML_SERIAL: cs_xml_serial,
    MethodsEnum.PYTHON_DESERIALIZATION_INJECTION: deserialization_injection,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if language_evaluator := METHOD_EVALUATORS.get(args.method):
        return language_evaluator(args)
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
