from api.schema import (
    SDL_CONTENT,
)
from graphql import (
    DirectiveNode,
    EnumTypeDefinitionNode,
    ObjectTypeDefinitionNode,
    parse,
)
from typing import (
    Optional,
)


def get_deprecation_reason(directives: list[DirectiveNode]) -> Optional[str]:
    return next(
        (
            directive.arguments[0].value.value
            for directive in directives
            if directive.name.value == "deprecated"
        ),
        None,
    )


def parse_schema_deprecations() -> None:
    schema_ast = parse(SDL_CONTENT)
    for definition in schema_ast.definitions:
        if isinstance(definition, EnumTypeDefinitionNode):
            for value in definition.values:
                deprecation_reason = get_deprecation_reason(value.directives)
                if deprecation_reason:
                    print(
                        definition.kind,
                        definition.name.value,
                        value.name.value,
                        deprecation_reason,
                    )

        if isinstance(definition, ObjectTypeDefinitionNode):
            for field in definition.fields:
                deprecation_reason = get_deprecation_reason(field.directives)
                if deprecation_reason:
                    print(
                        definition.kind,
                        definition.name.value,
                        field.name.value,
                        deprecation_reason,
                    )
