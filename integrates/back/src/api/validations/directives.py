from graphql import (
    GraphQLError,
    TokenKind,
)
from graphql.language.parser import (
    Parser,
)
from settings.api import (
    API_MAX_DIRECTIVES,
)


def validate_directives(query: str) -> None:
    """
    This validation prevents the execution of queries containing an excessive
    amount of directives to prevent abuse.
    """

    class DirectivesParser(Parser):
        def parse_directives(self, is_const: bool) -> None:
            directives = 0

            while self.peek(TokenKind.AT):
                directives += 1

                if directives > API_MAX_DIRECTIVES:
                    raise GraphQLError("Exception - Max directives exceeded")

                self.parse_directive(is_const)

    ast_parser = DirectivesParser(query)
    ast_parser.parse_document()
