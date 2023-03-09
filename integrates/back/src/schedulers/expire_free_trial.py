from aioextensions import (
    collect,
)
from custom_exceptions import (
    InvalidManagedChange,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.groups.enums import (
    GroupManaged,
    GroupStateJustification,
)
from db_model.groups.types import (
    Group,
)
from db_model.trials.types import (
    Trial,
    TrialMetadataToUpdate,
)
from groups import (
    domain as groups_domain,
)
from mailer import (
    groups as groups_mail,
)
from organizations import (
    domain as orgs_domain,
)
from schedulers.common import (
    error,
    info,
)
from trials import (
    domain as trials_domain,
)

EMAIL_INTEGRATES = "integrates@fluidattacks.com"
REMOVAL_AFTER_EXPIRATION_DAYS = 30


async def _remove_expired_groups_data(
    loaders: Dataloaders,
    group: Group,
    trial: Trial,
) -> None:
    if (
        days_since_expiration := trials_domain.get_days_since_expiration(trial)
        <= REMOVAL_AFTER_EXPIRATION_DAYS
    ):
        return

    info(
        "Removing data for group %s, created_by %s, start_date %s,"
        " days since expiration: %d",
        group.name,
        group.created_by,
        trial.start_date,
        days_since_expiration,
    )
    await groups_domain.remove_group(
        loaders=loaders,
        email=EMAIL_INTEGRATES,
        group_name=group.name,
        justification=GroupStateJustification.TRIAL_FINALIZATION,
        validate_pending_actions=False,
    )


async def _expire(
    loaders: Dataloaders,
    group: Group,
    trial: Trial,
) -> None:
    try:
        info(
            "Will expire group %s, created_by %s, start_date %s",
            group.name,
            group.created_by,
            trial.start_date,
        )
        await trials_domain.update_metadata(
            email=trial.email,
            metadata=TrialMetadataToUpdate(completed=True),
        )
        await groups_domain.update_group_managed(
            loaders=loaders,
            comments="Trial period has expired",
            email=EMAIL_INTEGRATES,
            group_name=group.name,
            justification=GroupStateJustification.TRIAL_FINALIZATION,
            managed=GroupManaged.UNDER_REVIEW,
        )
        await groups_mail.send_mail_free_trial_over(
            loaders=loaders,
            email_to=[group.created_by],
            group_name=group.name,
        )
    except InvalidManagedChange:
        error(
            "Couldn't expire group %s, managed %s",
            group.name,
            group.state.managed,
        )


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    groups = await orgs_domain.get_all_trial_groups(loaders)
    emails = [group.created_by for group in groups]
    trials = await loaders.trial.load_many(emails)

    await collect(
        tuple(
            _expire(loaders, group, trial)
            for group, trial in zip(groups, trials)
            if trial and trials_domain.has_expired(trial)
        )
    )

    await collect(
        tuple(
            _remove_expired_groups_data(loaders, group, trial)
            for group, trial in zip(groups, trials)
            if group.state.managed == GroupManaged.UNDER_REVIEW
            and trial
            and trial.completed
        ),
        workers=1,
    )
