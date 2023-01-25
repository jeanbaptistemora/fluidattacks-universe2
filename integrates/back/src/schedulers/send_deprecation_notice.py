from api.schema import (
    SDL_CONTENT,
)
from calendar import (
    monthrange,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model import (
    stakeholders as stakeholders_model,
)
from forces.domain import (
    is_forces_user,
)
from mailer.deprecations import (
    send_mail_deprecation_notice,
)
from newutils.datetime import (
    get_now_plus_delta,
)
from newutils.deprecations import (
    ApiDeprecation,
    get_deprecations_by_period,
)


def _format_deprecation_for_mail(
    deprecations: dict[str, list[ApiDeprecation]]
) -> dict[str, str]:
    """
    Translates the deprecation dict values to a more readable mail format
    """
    depr_mail: dict[str, str] = {}
    for key, deprecated_fields in deprecations.items():
        depr_mail[key] = " | ".join(
            [field.field for field in deprecated_fields]
        )

    return depr_mail


async def main() -> None:
    # We gather all deprecations due for the last day of the next month
    next_month: datetime = get_now_plus_delta(weeks=4)
    last_day: int = monthrange(next_month.year, next_month.month)[1]
    deprecations = get_deprecations_by_period(
        sdl_content=SDL_CONTENT,
        end=next_month.replace(day=last_day),
        start=next_month.replace(day=1),
    )
    if bool(deprecations):
        mail_deprecations: dict[str, str] = _format_deprecation_for_mail(
            deprecations
        )
        # Find users with generated tokens
        all_stakeholders = await stakeholders_model.get_all_stakeholders()
        users_with_tokens: set[str] = {
            stakeholder.email
            for stakeholder in all_stakeholders
            if stakeholder.access_token is not None
            and not is_forces_user(stakeholder.email)
        }
        # Send out the mails
        loaders: Dataloaders = get_new_context()
        await send_mail_deprecation_notice(
            loaders=loaders,
            mail_deprecations=mail_deprecations,
            email_to=users_with_tokens,
        )
