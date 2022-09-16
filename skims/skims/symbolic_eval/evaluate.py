# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.core_model import (
    MethodsEnum,
)
from model.graph_model import (
    Graph,
    NId,
)
from symbolic_eval.cases import (
    argument_list,
    array_initializer,
    assignment,
    binary_operation,
    call_expression,
    element_access,
    execution_block,
    field_declaration,
    for_each_statement,
    if_statement,
    interpolated_string_expression,
    lambda_expression,
    literal,
    member_access,
    method_declaration,
    method_invocation,
    named_argument,
    new_expression,
    object_creation,
    object_node,
    pair,
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
    "ArrayInitializer": array_initializer.evaluate,
    "Assignment": assignment.evaluate,
    "BinaryOperation": binary_operation.evaluate,
    "CallExpression": call_expression.evaluate,
    "ElementAccess": element_access.evaluate,
    "ElementValuePair": named_argument.evaluate,
    "ExecutionBlock": execution_block.evaluate,
    "FieldDeclaration": field_declaration.evaluate,
    "ForEachStatement": for_each_statement.evaluate,
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
    "PrefixOperation": prefix_operation.evaluate,
    "SymbolLookup": symbol_lookup.evaluate,
    "TypeOf": type_of.evaluate,
    "VariableDeclaration": variable_declaration.evaluate,
    "VariableDeclarator": variable_declaration.evaluate,
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
