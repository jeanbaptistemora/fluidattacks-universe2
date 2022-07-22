from api.schema import (
    SDL_CONTENT,
)
from api.utils.types import (
    ApiDeprecation,
)
from graphql import (
    DirectiveNode,
    DocumentNode,
    EnumTypeDefinitionNode,
    InputObjectTypeDefinitionNode,
    ObjectTypeDefinitionNode,
    parse,
    TypeDefinitionNode,
)
from typing import (
    Optional,
)


def _get_deprecation_reason(directives: list[DirectiveNode]) -> Optional[str]:
    return next(
        (
            directive.arguments[0].value.value
            for directive in directives
            if directive.name.value == "deprecated"
        ),
        None,
    )


def _search_directives(
    definition: TypeDefinitionNode,
    deprecations: dict[str, list[ApiDeprecation]],
    has_arguments: bool,
) -> dict[str, list[ApiDeprecation]]:

    if isinstance(definition, EnumTypeDefinitionNode):
        fields = definition.values
    elif isinstance(definition, ObjectTypeDefinitionNode):
        fields = definition.fields
    elif isinstance(definition, InputObjectTypeDefinitionNode):
        fields = definition.fields
    else:
        fields = []

    for field in fields:
        deprecation_reason = _get_deprecation_reason(field.directives)
        if deprecation_reason:
            deprecations.setdefault(definition.name.value, []).append(
                ApiDeprecation(
                    parent=definition.name.value,
                    field=field.name.value,
                    reason=deprecation_reason.replace("\n", " "),
                    type=definition.kind,
                )
            )
        if has_arguments:
            for argument in field.arguments:
                arg_deprecation = _get_deprecation_reason(argument.directives)
                if arg_deprecation:
                    deprecations.setdefault(definition.name.value, []).append(
                        ApiDeprecation(
                            parent=definition.name.value,
                            field=argument.name.value,
                            reason=arg_deprecation.replace("\n", " "),
                            type=definition.kind,
                        )
                    )
    return deprecations


def parse_schema_deprecations() -> None:
    schema_ast: DocumentNode = parse(SDL_CONTENT)
    enums: dict[str, list[ApiDeprecation]] = {}
    operations: dict[str, list[ApiDeprecation]] = {}

    for definition in schema_ast.definitions:
        if isinstance(definition, EnumTypeDefinitionNode):
            _search_directives(definition, enums, False)

        if has_arguments := isinstance(definition, ObjectTypeDefinitionNode):
            _search_directives(definition, operations, has_arguments)

        if isinstance(definition, InputObjectTypeDefinitionNode):
            _search_directives(definition, operations, False)
