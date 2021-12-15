from model.core_model import (
    FindingEnum,
)
from model.graph_model import (
    Graph,
    GraphShardMetadataLanguage as GraphLanguage,
    NId,
)
from symbolic_eval.cases import (
    argument_list,
    binary_operation,
    element_access,
    execution_block,
    if_statement,
    literal,
    member_access,
    method_declaration,
    method_invocation,
    object_creation,
    parameter,
    parameter_list,
    prefix_operation,
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
from utils import (
    logs,
)

EVALUATORS: Dict[str, Evaluator] = {
    "ArgumentList": argument_list.evaluate,
    "BinaryOperation": binary_operation.evaluate,
    "ElementAccess": element_access.evaluate,
    "ExecutionBlock": execution_block.evaluate,
    "If": if_statement.evaluate,
    "Literal": literal.evaluate,
    "MemberAccess": member_access.evaluate,
    "MethodDeclaration": method_declaration.evaluate,
    "MethodInvocation": method_invocation.evaluate,
    "ObjectCreation": object_creation.evaluate,
    "Parameter": parameter.evaluate,
    "ParameterList": parameter_list.evaluate,
    "PrefixOperation": prefix_operation.evaluate,
    "SymbolLookup": symbol_lookup.evaluate,
    "VariableDeclaration": variable_declaration.evaluate,
}


def generic(args: SymbolicEvalArgs) -> bool:
    node_type = args.graph.nodes[args.n_id]["label_type"]
    evaluator = EVALUATORS.get(node_type)

    if not evaluator:
        raise MissingSymbolicEval(f"Missing symbolic evaluator {node_type}")

    if args.n_id in args.evaluation:
        return args.evaluation[args.n_id]

    return evaluator(args)


def evaluate(
    language: GraphLanguage,
    finding: FindingEnum,
    graph: Graph,
    path: Path,
    n_id: NId,
) -> Optional[bool]:
    try:
        evaluation: Dict[NId, bool] = {}

        return generic(
            SymbolicEvalArgs(
                generic, language, finding, evaluation, graph, path, n_id
            )
        )
    except MissingSymbolicEval as error:
        logs.log_blocking("warning", error)
        return None
