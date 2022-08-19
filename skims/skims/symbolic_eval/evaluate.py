from model.core_model import (
    MethodsEnum,
)
from model.graph_model import (
    Graph,
    NId,
)
from symbolic_eval.cases import (
    argument_list,
    assignment,
    binary_operation,
    element_access,
    execution_block,
    if_statement,
    interpolated_string_expression,
    lambda_expression,
    literal,
    member_access,
    method_declaration,
    method_invocation,
    named_argument,
    object_creation,
    parameter,
    parameter_list,
    prefix_operation,
    symbol_lookup,
    type_of,
    variable_declaration,
)
from symbolic_eval.types import (
    Evaluator,
    MissingSymbolicEval,
    Path,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)
from typing import (
    cast,
    Dict,
    Optional,
)
from utils import (
    logs,
)

EVALUATORS: Dict[str, Evaluator] = {
    "ArgumentList": argument_list.evaluate,
    "Assignment": assignment.evaluate,
    "BinaryOperation": binary_operation.evaluate,
    "ElementAccess": element_access.evaluate,
    "ExecutionBlock": execution_block.evaluate,
    "If": if_statement.evaluate,
    "InterpolatedStringExpression": interpolated_string_expression.evaluate,
    "LambdaExpression": lambda_expression.evaluate,
    "Literal": literal.evaluate,
    "MemberAccess": member_access.evaluate,
    "MethodDeclaration": method_declaration.evaluate,
    "MethodInvocation": method_invocation.evaluate,
    "NamedArgument": named_argument.evaluate,
    "ObjectCreation": object_creation.evaluate,
    "Parameter": parameter.evaluate,
    "ParameterList": parameter_list.evaluate,
    "PrefixOperation": prefix_operation.evaluate,
    "SymbolLookup": symbol_lookup.evaluate,
    "TypeOf": type_of.evaluate,
    "VariableDeclaration": variable_declaration.evaluate,
}


def generic(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    node_type = args.graph.nodes[args.n_id]["label_type"]
    evaluator = EVALUATORS.get(node_type)

    if not evaluator:
        raise MissingSymbolicEval(f"Missing symbolic evaluator {node_type}")

    if args.n_id in args.evaluation:
        return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)

    return evaluator(args)


def evaluate(
    method: MethodsEnum,
    graph: Graph,
    path: Path,
    n_id: NId,
) -> Optional[SymbolicEvaluation]:
    try:
        evaluation: Dict[NId, bool] = {}

        return generic(
            SymbolicEvalArgs(
                generic, method, evaluation, graph, path, n_id, set()
            )
        )
    except MissingSymbolicEval as error:
        logs.log_blocking("warning", cast(str, error))
        return None
