from custom_exceptions import (
    InvalidDateFormat,
)
from datetime import (
    datetime,
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
from newutils import (
    datetime as date_utils,
)
from newutils.deprecations.filters import (
    filter_api_deprecation_dict,
)
from newutils.deprecations.types import (
    ApiDeprecation,
)
from re import (
    search,
)
from typing import (
    Optional,
)


def get_due_date(definition: str, field: str, reason: str) -> datetime:
    """
    Searches the deprecation reason for a date in the format `YYYY/MM/DD`.
    If none is found, raises an error
    """
    match = search(r"\d{4}/\d{2}/\d{2}", reason)
    if match:
        return date_utils.get_from_str(match.group(), "%Y/%m/%d")
    raise InvalidDateFormat(
        expr=(
            "No deprecation date in the format YYYY/MM/DD found in reason "
            f"'{reason}' of field {field} from definition {definition}"
        )
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
                    due_date=get_due_date(
                        definition=definition.name.value,
                        field=field.name.value,
                        reason=deprecation_reason.replace("\n", " "),
                    ),
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
                            due_date=get_due_date(
                                definition=definition.name.value,
                                field=field.name.value,
                                reason=arg_deprecation.replace("\n", " "),
                            ),
                            type=definition.kind,
                        )
                    )
    return deprecations


def parse_schema_deprecations(
    sdl_content: str,
) -> tuple[dict[str, list[ApiDeprecation]], dict[str, list[ApiDeprecation]]]:
    """Parses the SDL content and returns a couple of dicts (`enums`,
    `operations`) with all the deprecations found in the respective schema"""
    schema_ast: DocumentNode = parse(sdl_content)
    enums: dict[str, list[ApiDeprecation]] = {}
    operations: dict[str, list[ApiDeprecation]] = {}

    for definition in schema_ast.definitions:
        if isinstance(definition, EnumTypeDefinitionNode):
            _search_directives(definition, enums, False)

        if has_arguments := isinstance(definition, ObjectTypeDefinitionNode):
            _search_directives(definition, operations, has_arguments)

        if isinstance(definition, InputObjectTypeDefinitionNode):
            _search_directives(definition, operations, False)
    return (enums, operations)


def get_deprecations_by_period(
    sdl_content: str, end: datetime, start: Optional[datetime]
) -> tuple[dict[str, list[ApiDeprecation]], dict[str, list[ApiDeprecation]]]:
    """
    Gets the deprecations found in the schema within a time period. The first
    member of the tuple corresponding to `enum` deprecations and the latter to
    `operations` e.g. mutation, queries, args, inputs etc...
    """
    (enums, operations) = parse_schema_deprecations(sdl_content)
    return (
        filter_api_deprecation_dict(enums, end, start),
        filter_api_deprecation_dict(operations, end, start),
    )
