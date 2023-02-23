from custom_exceptions import (
    InvalidDateFormat,
)
from datetime import (
    datetime,
)
from graphql import (
    DirectiveDefinitionNode,
    DirectiveNode,
    DocumentNode,
    EnumTypeDefinitionNode,
    InputObjectTypeDefinitionNode,
    ObjectTypeDefinitionNode,
    parse,
    TypeDefinitionNode,
)
from newutils import (
    datetime as datetime_utils,
)
from newutils.deprecations.filters import (
    filter_api_deprecation_dict,
)
from newutils.deprecations.types import (
    ApiDeprecation,
    ApiFieldType,
)
from re import (
    search,
)


def get_due_date(definition: str, field: str, reason: str) -> datetime:
    """
    Searches the deprecation reason for a date in the format `YYYY/MM/DD`.
    If none is found, raises an error
    """
    match = search(r"\d{4}/\d{2}/\d{2}", reason)
    if match:
        return datetime_utils.get_from_str(match.group(), "%Y/%m/%d")
    raise InvalidDateFormat(
        expr=(
            "No deprecation date in the format YYYY/MM/DD found in reason "
            f"'{reason}' of field {field} from definition {definition}"
        )
    )


def _get_deprecation_reason(directives: list[DirectiveNode]) -> str | None:
    return next(
        (
            directive.arguments[0].value.value  # type: ignore
            for directive in directives
            if directive.name.value == "deprecated"
        ),
        None,
    )


def _search_directives(
    definition: TypeDefinitionNode | DirectiveDefinitionNode,
    deprecations: dict[str, list[ApiDeprecation]],
    has_arguments: bool,
) -> dict[str, list[ApiDeprecation]]:

    if isinstance(definition, EnumTypeDefinitionNode):
        fields = definition.values
    elif isinstance(definition, ObjectTypeDefinitionNode):
        fields = definition.fields  # type: ignore
    elif isinstance(definition, InputObjectTypeDefinitionNode):
        fields = definition.fields  # type: ignore
    # Custom directives do not have fields, but they have arguments
    # Might be a good idea to rethink the control flow a little
    elif isinstance(definition, DirectiveDefinitionNode):
        fields = definition.arguments  # type: ignore
    else:
        fields = []  # type: ignore

    for field in fields:
        deprecation_reason = _get_deprecation_reason(
            field.directives  # type: ignore
        )
        if deprecation_reason:
            deprecations.setdefault(definition.name.value, []).append(
                ApiDeprecation(
                    parent=definition.name.value,
                    field=field.name.value,
                    reason=deprecation_reason.replace("\n", " "),
                    due_date=get_due_date(
                        definition=definition.name.value,
                        field=field.name.value,
                        reason=deprecation_reason.replace("\n", " "),
                    ),
                    type=ApiFieldType(definition.kind),
                )
            )
        if has_arguments:
            for argument in field.arguments:  # type: ignore
                arg_deprecation = _get_deprecation_reason(argument.directives)
                if arg_deprecation:
                    deprecations.setdefault(definition.name.value, []).append(
                        ApiDeprecation(
                            parent=definition.name.value,
                            field=argument.name.value,
                            reason=arg_deprecation.replace("\n", " "),
                            due_date=get_due_date(
                                definition=definition.name.value,
                                field=field.name.value,
                                reason=arg_deprecation.replace("\n", " "),
                            ),
                            type=ApiFieldType(definition.kind),
                        )
                    )
    return deprecations


def _parse_schema_deprecations(
    sdl_content: str,
) -> dict[str, list[ApiDeprecation]]:
    """Parses the SDL content and returns a couple of dicts (`enums`,
    `operations`) with all the deprecations found in the respective schema"""
    schema_ast: DocumentNode = parse(sdl_content)
    deprecations: dict[str, list[ApiDeprecation]] = {}

    for definition in schema_ast.definitions:
        if isinstance(definition, EnumTypeDefinitionNode):
            _search_directives(definition, deprecations, False)

        elif isinstance(definition, DirectiveDefinitionNode):
            _search_directives(definition, deprecations, False)

        elif isinstance(definition, InputObjectTypeDefinitionNode):
            _search_directives(definition, deprecations, False)

        elif has_arguments := isinstance(definition, ObjectTypeDefinitionNode):
            _search_directives(definition, deprecations, has_arguments)

        else:
            # pass statement for now
            pass
    return deprecations


def get_deprecations_by_period(
    sdl_content: str, end: datetime, start: datetime | None
) -> dict[str, list[ApiDeprecation]]:
    """
    Gets the deprecations found in the schema within a time period
    """
    all_deprecations = _parse_schema_deprecations(sdl_content)
    return filter_api_deprecation_dict(all_deprecations, end, start)
