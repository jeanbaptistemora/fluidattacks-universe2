from model.core_model import (
    MethodsEnum,
)
from model.graph_model import (
    Graph,
    NId,
)
from symbolic_eval.cases import (
    argument,
    argument_list,
    array_access,
    array_creation,
    array_initializer,
    assignment,
    await_expression,
    binary_operation,
    cast_expression,
    element_access,
    else_clause,
    execution_block,
    expression_statement,
    field_declaration,
    for_each_statement,
    for_statement,
    if_statement,
    interpolated_string_expression,
    lambda_expression,
    literal,
    member_access,
    method_declaration,
    method_invocation,
    named_argument,
    new_expression,
    not_dangerous,
    object_creation,
    object_node,
    pair,
    parameter,
    parameter_list,
    parenthesized_expression,
    prefix_operation,
    return_node,
    spread_element,
    switch_case,
    symbol_lookup,
    ternary_operation,
    try_statement,
    type_of,
    unary_expression,
    using_statement,
    variable_declaration,
    while_statement,
)
from symbolic_eval.types import (
    Evaluator,
    MissingSymbolicEval,
    Path,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)
from symbolic_eval.utils import (
    get_backward_paths,
)
from typing import (
    cast,
)
from utils import (
    logs,
)

EVALUATORS: dict[str, Evaluator] = {
    "Argument": argument.evaluate,
    "ArgumentList": argument_list.evaluate,
    "ArrayAccess": array_access.evaluate,
    "ArrayCreation": array_creation.evaluate,
    "ArrayInitializer": array_initializer.evaluate,
    "Assignment": assignment.evaluate,
    "AwaitExpression": await_expression.evaluate,
    "Break": not_dangerous.evaluate,
    "Comment": not_dangerous.evaluate,
    "Continue": not_dangerous.evaluate,
    "ClassBody": not_dangerous.evaluate,
    "BinaryOperation": binary_operation.evaluate,
    "CastExpression": cast_expression.evaluate,
    "ElementAccess": element_access.evaluate,
    "ElementValuePair": named_argument.evaluate,
    "ElseClause": else_clause.evaluate,
    "ExecutionBlock": execution_block.evaluate,
    "ExpressionStatement": expression_statement.evaluate,
    "FieldDeclaration": field_declaration.evaluate,
    "ForEachStatement": for_each_statement.evaluate,
    "ForStatement": for_statement.evaluate,
    "If": if_statement.evaluate,
    "InterpolatedStringExpression": interpolated_string_expression.evaluate,
    "LambdaExpression": lambda_expression.evaluate,
    "Literal": literal.evaluate,
    "NewExpression": new_expression.evaluate,
    "MemberAccess": member_access.evaluate,
    "MethodDeclaration": method_declaration.evaluate,
    "MethodInvocation": method_invocation.evaluate,
    "NamedArgument": named_argument.evaluate,
    "Object": object_node.evaluate,
    "ObjectCreation": object_creation.evaluate,
    "Pair": pair.evaluate,
    "Parameter": parameter.evaluate,
    "ParameterList": parameter_list.evaluate,
    "ParenthesizedExpression": parenthesized_expression.evaluate,
    "PrefixOperation": prefix_operation.evaluate,
    "Return": return_node.evaluate,
    "ReservedWord": not_dangerous.evaluate,
    "SpreadElement": spread_element.evaluate,
    "SwitchBody": switch_case.evaluate,
    "SwitchSection": switch_case.evaluate,
    "SwitchStatement": switch_case.evaluate,
    "SymbolLookup": symbol_lookup.evaluate,
    "TernaryOperation": ternary_operation.evaluate,
    "TryStatement": try_statement.evaluate,
    "This": not_dangerous.evaluate,
    "TypeOf": type_of.evaluate,
    "UnaryExpression": unary_expression.evaluate,
    "UsingStatement": using_statement.evaluate,
    "VariableDeclaration": variable_declaration.evaluate,
    "VariableDeclarator": variable_declaration.evaluate,
    "WhileStatement": while_statement.evaluate,
    "Yield": not_dangerous.evaluate,
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
) -> SymbolicEvaluation | None:
    try:
        evaluation: dict[NId, bool] = {}
        return generic(
            SymbolicEvalArgs(
                generic, method, evaluation, graph, path, n_id, set()
            )
        )
    except MissingSymbolicEval as error:
        logs.log_blocking("debug", cast(str, error))
        return None


def get_node_evaluation_results(
    method: MethodsEnum,
    graph: Graph,
    n_id: NId,
    triggers_goal: set[str],
    danger_goal: bool = True,
) -> bool:
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if (
            evaluation
            and evaluation.danger == danger_goal
            and evaluation.triggers == triggers_goal
        ):
            return True
    return False
