# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from api import (
    Operation,
)
from graphql import (
    GraphQLError,
    ValidationContext,
    ValidationRule,
)
from settings.api import (
    API_MAX_CHARACTERS,
)
from typing import (
    Any,
)


def validate_characters(context_value: Any) -> ValidationRule:
    """
    This validation prevents the execution of queries containing an excessive
    amount characters to prevent abuse.
    """
    operation: Operation = context_value.operation

    class CharactersThresholdValidation(ValidationRule):
        def __init__(self, context: ValidationContext) -> None:
            super().__init__(context)

            if len(operation.query) > API_MAX_CHARACTERS:
                self.report_error(
                    GraphQLError("Exception - Max characters exceeded")
                )

    return CharactersThresholdValidation
