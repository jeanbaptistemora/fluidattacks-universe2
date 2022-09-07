# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from graphql import (
    GraphQLError,
    OperationDefinitionNode,
    ValidationRule,
)
from typing import (
    Any,
)


def variables_check(context_value: Any) -> ValidationRule:
    """
    This validation prevents the execution of operation containing not defined
    variables.
    """

    class VariableValidation(ValidationRule):
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

    return VariableValidation
