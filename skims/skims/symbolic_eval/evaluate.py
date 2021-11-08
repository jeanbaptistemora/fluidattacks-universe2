from model.core_model import (
    FindingEnum,
)
from model.graph_model import (
    Graph,
    GraphShardMetadataLanguage as GraphLanguage,
)
from symbolic_eval.cases import (
    argument_list,
    binary_operation,
    element_access,
    literal,
    member_access,
    method_declaration,
    method_invocation,
    parameter,
    parameter_list,
    symbol_lookup,
    variable_declaration,
)
from symbolic_eval.types import (
    Evaluator,
    MissingSymbolicEval,
    Path,
    SymbolicEvalArgs,
)
from typing import (
    Dict,
    Optional,
)

EVALUATORS: Dict[str, Evaluator] = {
    "ArgumentList": argument_list.evaluate,
    "BinaryOperation": binary_operation.evaluate,
    "ElementAccess": element_access.evaluate,
    "Literal": literal.evaluate,
    "MemberAccess": member_access.evaluate,
    "MethodDeclaration": method_declaration.evaluate,
    "MethodInvocation": method_invocation.evaluate,
    "Parameter": parameter.evaluate,
    "ParameterList": parameter_list.evaluate,
    "SymbolLookup": symbol_lookup.evaluate,
    "VariableDeclaration": variable_declaration.evaluate,
}


def generic(args: SymbolicEvalArgs) -> bool:
    node_type = args.graph.nodes[args.n_id]["label_type"]
    if evaluator := EVALUATORS.get(node_type):
        return evaluator(args)
    raise MissingSymbolicEval(f"Missing symbolic evaluator for {node_type}")


def evaluate(
    lang: GraphLanguage,
    finding: FindingEnum,
    graph: Graph,
    path: Path,
    n_id: str,
) -> Optional[bool]:
    try:
        args = SymbolicEvalArgs(generic, lang, finding, graph, path, n_id)
        return generic(args)
    except MissingSymbolicEval as error:
        print(error)
        return None
