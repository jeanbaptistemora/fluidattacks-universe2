from api.types import (
    Operation,
)
from graphql import (
    ASTValidationRule,
    GraphQLError,
    ValidationContext,
)
from settings.api import (
    API_MAX_CHARACTERS,
)
from typing import (
    Any,
)


def validate_characters(context_value: Any) -> ASTValidationRule:
    """
    This validation prevents the execution of queries containing an excessive
    amount characters to prevent abuse.
    """
    operation: Operation = context_value.operation

    class CharactersThresholdValidation(ASTValidationRule):
        def __init__(self, context: ValidationContext) -> None:
            super().__init__(context)

            if len(operation.query) > API_MAX_CHARACTERS:
                self.report_error(
                    GraphQLError("Exception - Max characters exceeded")
                )

    return CharactersThresholdValidation  # type: ignore
