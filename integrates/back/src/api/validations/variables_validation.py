from graphql import (
    ASTValidationRule,
    GraphQLError,
    OperationDefinitionNode,
)
from typing import (
    Any,
)


def variables_check(context_value: Any) -> ASTValidationRule:
    """
    This validation prevents the execution of operation containing not defined
    variables.
    """

    class VariableValidation(ASTValidationRule):
        def enter_operation_definition(
            self, node: OperationDefinitionNode, *_args: Any
        ) -> None:
            if node.variable_definitions:
                operation_variables = [
                    item.variable.name.value
                    for item in node.variable_definitions
                ]
                client_variables = context_value.operation.variables.keys()
                for item in client_variables:
                    if item not in operation_variables:
                        self.report_error(
                            GraphQLError(
                                "Exception - Extra variables in operation",
                                node,
                            )
                        )

    return VariableValidation  # type: ignore
