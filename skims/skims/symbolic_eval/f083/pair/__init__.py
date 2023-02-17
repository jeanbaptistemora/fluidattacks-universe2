from model.core_model import (
    MethodsEnum,
)
from symbolic_eval.f083.pair.common import (
    generic_xml_parser,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

METHOD_EVALUATORS: dict[MethodsEnum, Evaluator] = {
    MethodsEnum.JS_XML_PARSER: generic_xml_parser,
    MethodsEnum.TS_XML_PARSER: generic_xml_parser,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if language_evaluator := METHOD_EVALUATORS.get(args.method):
        return language_evaluator(args)
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
