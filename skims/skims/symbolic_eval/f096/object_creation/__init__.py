from model.core_model import (
    MethodsEnum,
)
from symbolic_eval.f096.object_creation.c_sharp import (
    cs_js_deserialization,
    cs_xml_serial,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

METHOD_EVALUATORS: dict[MethodsEnum, Evaluator] = {
    MethodsEnum.CS_JS_DESERIALIZATION: cs_js_deserialization,
    MethodsEnum.CS_XML_SERIAL: cs_xml_serial,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if language_evaluator := METHOD_EVALUATORS.get(args.method):
        return language_evaluator(args)
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
