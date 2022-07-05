from graphql import (
    DocumentNode,
    GraphQLSchema,
    NoFragmentCyclesRule,
    validate,
)


def validate_fragments(
    schema: GraphQLSchema,
    document_ast: DocumentNode,
) -> None:
    """
    This validation prevents the execution of queries containing recursive
    fragments to prevent abuse.
    """
    errors = validate(schema, document_ast, rules=[NoFragmentCyclesRule])

    if errors:
        raise errors[0]
