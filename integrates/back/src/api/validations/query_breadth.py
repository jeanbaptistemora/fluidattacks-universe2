from graphql import (
    GraphQLError,
    OperationDefinitionNode,
    ValidationRule,
)
from settings.api import (
    API_MAX_QUERY_BREADTH,
)
from typing import (
    Any,
)


class QueryBreadthValidation(ValidationRule):
    """
    This validation prevents the execution of queries requesting an excessive
    amount of root resolvers to prevent abuse.
    """

    def enter_operation_definition(
        self, node: OperationDefinitionNode, *_args: Any
    ) -> None:
        if len(node.selection_set.selections) > API_MAX_QUERY_BREADTH:
            self.report_error(
                GraphQLError("Exception - Max query breadth exceeded", node)
            )
