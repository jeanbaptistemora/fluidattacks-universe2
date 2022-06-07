from api import (
    APP_EXCEPTIONS,
)
from ariadne import (
    convert_kwargs_to_snake_case,
)
from custom_exceptions import (
    InvalidSortsParameters,
)
from custom_types import (
    SimplePayload as SimplePayloadType,
)
from dataloaders import (
    Dataloaders,
)
from db_model.roots.types import (
    Root,
)
from db_model.toe_lines.types import (
    SortsSuggestion,
    ToeLines,
    ToeLinesRequest,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    logs as logs_utils,
)
from operator import (
    attrgetter,
)
from roots import (
    domain as roots_domain,
)
from toe.lines import (
    domain as toe_lines_domain,
)
from toe.lines.types import (
    ToeLinesAttributesToUpdate,
)
from toe.lines.validations import (
    validate_sort_risk_level,
    validate_sort_suggestions,
)
from typing import (
    Any,
    Optional,
)


def _format_sorts_suggestions(
    suggestions: list[dict[str, Any]]
) -> list[SortsSuggestion]:
    unordered = [
        SortsSuggestion(
            finding_title=item["finding_title"],
            probability=item["probability"],
        )
        for item in suggestions
    ]
    return sorted(unordered, key=attrgetter("probability"), reverse=True)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
async def mutate(  # pylint: disable=too-many-arguments
    _: Any,
    info: GraphQLResolveInfo,
    group_name: str,
    root_nickname: str,
    filename: str,
    sorts_risk_level: Optional[int] = None,
    sorts_suggestions: Optional[list[dict[str, Any]]] = None,
) -> SimplePayloadType:
    if sorts_risk_level is None and sorts_suggestions is None:
        raise InvalidSortsParameters.new()

    if sorts_risk_level is not None:
        validate_sort_risk_level(sorts_risk_level)

    sorts_suggestions_formatted = None
    if sorts_suggestions is not None:
        sorts_suggestions_formatted = _format_sorts_suggestions(
            sorts_suggestions
        )
        await validate_sort_suggestions(sorts_suggestions_formatted)

    try:
        loaders: Dataloaders = info.context.loaders
        roots: tuple[Root, ...] = await loaders.group_roots.load(group_name)
        root_id = roots_domain.get_root_id_by_nickname(
            root_nickname, roots, only_git_roots=True
        )
        toe_lines: ToeLines = await loaders.toe_lines.load(
            ToeLinesRequest(
                filename=filename, group_name=group_name, root_id=root_id
            )
        )
        await toe_lines_domain.update(
            toe_lines,
            ToeLinesAttributesToUpdate(
                sorts_risk_level=sorts_risk_level,
                sorts_suggestions=sorts_suggestions_formatted,
            ),
        )
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Updated sorts parameters for group {group_name} in "
            f"root {root_nickname} in toes with filename {filename} "
            f"successfully",
        )
    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Tried to update sorts parameters for group "
            f"{group_name} in root {root_nickname} in toes with "
            f"filename {filename}",
        )
        raise

    return SimplePayloadType(success=True)
