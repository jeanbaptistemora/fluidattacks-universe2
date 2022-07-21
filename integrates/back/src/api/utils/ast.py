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
    deprecation_dict: dict[str, set[ApiDeprecation]],
) -> dict[str, set[ApiDeprecation]]:

    if isinstance(definition, EnumTypeDefinitionNode):
        fields = definition.values
    elif isinstance(definition, ObjectTypeDefinitionNode):
        fields = definition.fields
    elif isinstance(definition, InputObjectTypeDefinitionNode):
        fields = definition.fields
    else:
        fields = []

    for value in fields:
        deprecation_reason = _get_deprecation_reason(value.directives)
        if deprecation_reason:
            deprecation_dict.setdefault(definition.name.value, set()).add(
                ApiDeprecation(
                    parent=definition.name.value,
                    field=value.name.value,
                    reason=deprecation_reason.replace("\n", " "),
                )
            )
    return deprecation_dict


def _search_field_arguments(
    definition: ObjectTypeDefinitionNode,
    deprecation_dict: dict[str, set[ApiDeprecation]],
) -> dict[str, set[ApiDeprecation]]:
    for field in definition.fields:
        for argument in field.arguments:
            arg_deprecation = _get_deprecation_reason(argument.directives)
            if arg_deprecation:
                deprecation_dict.setdefault(definition.name.value, set()).add(
                    ApiDeprecation(
                        parent=definition.name.value,
                        field=argument.name.value,
                        reason=arg_deprecation.replace("\n", " "),
                    )
                )
    return deprecation_dict


def parse_schema_deprecations() -> None:
    schema_ast: DocumentNode = parse(SDL_CONTENT)
    arguments: dict[str, set[ApiDeprecation]] = {}
    enums: dict[str, set[ApiDeprecation]] = {}
    operations: dict[str, set[ApiDeprecation]] = {}

    for definition in schema_ast.definitions:
        if isinstance(definition, EnumTypeDefinitionNode):
            _search_directives(definition, enums)

        if isinstance(definition, ObjectTypeDefinitionNode):
            _search_directives(definition, operations)
            _search_field_arguments(definition, arguments)

        if isinstance(definition, InputObjectTypeDefinitionNode):
            _search_directives(definition, arguments)
