from graphql import (
    FieldNode,
    GraphQLError,
    ValidationContext,
    ValidationRule,
)
from settings.api import (
    GRAPHQL_MAX_QUERY_DEPTH,
)
from typing import (
    Any,
)


class QueryDepthValidation(ValidationRule):
    """
    This validation prevents the execution of queries containing an excessive
    amount of nested cyclic resolvers to prevent abuse.

    Inspired by graphql-ruby's implementation
    """

    def __init__(self, context: ValidationContext) -> None:
        super().__init__(context)
        self.current_depth = 0

    def enter_field(self, *_: Any) -> None:
        self.current_depth += 1

    def leave_field(self, node: FieldNode, *_: Any) -> None:
        if self.current_depth > GRAPHQL_MAX_QUERY_DEPTH:
            self.report_error(
                GraphQLError("Exception - Max query depth exceeded", node)
            )

        self.current_depth -= 1
