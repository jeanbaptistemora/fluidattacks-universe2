from .payloads.types import (
    SimplePayload,
)
from api import (
    APP_EXCEPTIONS,
)
from ariadne import (
    convert_kwargs_to_snake_case,
)
from custom_exceptions import (
    InvalidSortsParameters,
    ToeLinesNotFound,
)
from dataloaders import (
    Dataloaders,
)
from datetime import (
    datetime,
)
from db_model.toe_lines.types import (
    SortsSuggestion,
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
    validate_sorts_risk_level_date,
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
    sorts_risk_level_date: Optional[datetime] = None,
    sorts_suggestions: Optional[list[dict[str, Any]]] = None,
) -> SimplePayload:
    loaders: Dataloaders = info.context.loaders
    if (
        sorts_risk_level is None
        and sorts_suggestions is None
        and sorts_risk_level_date is None
    ):
        raise InvalidSortsParameters.new()

    if sorts_risk_level is not None:
        validate_sort_risk_level(sorts_risk_level)

    if sorts_risk_level_date is not None:
        validate_sorts_risk_level_date(sorts_risk_level_date)

    sorts_suggestions_formatted = None
    if sorts_suggestions is not None:
        sorts_suggestions_formatted = _format_sorts_suggestions(
            sorts_suggestions
        )
        await validate_sort_suggestions(loaders, sorts_suggestions_formatted)

    try:
        roots = await loaders.group_roots.load(group_name)
        root_id = roots_domain.get_root_id_by_nickname(
            root_nickname, tuple(roots), only_git_roots=True
        )
        toe_lines = await loaders.toe_lines.load(
            ToeLinesRequest(
                filename=filename, group_name=group_name, root_id=root_id
            )
        )
        if toe_lines is None:
            raise ToeLinesNotFound()

        await toe_lines_domain.update(
            toe_lines,
            ToeLinesAttributesToUpdate(
                sorts_risk_level=sorts_risk_level,
                sorts_risk_level_date=sorts_risk_level_date,
                sorts_suggestions=sorts_suggestions_formatted,
            ),
        )
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Updated sorts parameters for group {group_name} in "
            f"root {root_nickname} in toes with filename {filename} "
            "successfully",
        )
    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context,
            "Security: Tried to update sorts parameters for group "
            f"{group_name} in root {root_nickname} in toes with "
            f"filename {filename}",
        )
        raise

    return SimplePayload(success=True)
