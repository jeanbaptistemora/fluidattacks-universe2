from dataloaders import (
    Dataloaders,
)
from db_model.companies.types import (
    Company,
    Trial,
)
from db_model.enrollment.types import (
    Enrollment,
    Trial as EnrollmentTrial,
)
from enrollment import (
    domain as enrollment_domain,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    datetime as datetime_utils,
)
from typing import (
    Any,
    cast,
    Optional,
)


async def resolve(
    parent: Enrollment,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> dict[str, Any]:
    loaders: Dataloaders = info.context.loaders
    domain = parent.email.split("@")[1]
    company: Optional[Company] = await loaders.company.load(domain)
    trial = (
        company.trial
        if company
        else Trial(
            completed=False,
            extension_date="",
            extension_days=0,
            start_date="",
        )
    )

    return {
        "completed": trial.completed,
        "extension_date": datetime_utils.convert_from_iso_str(
            trial.extension_date
        )
        if trial.extension_date
        else "",
        "extension_days": trial.extension_days,
        "start_date": datetime_utils.convert_from_iso_str(trial.start_date)
        if trial.start_date
        else "",
        "state": enrollment_domain.get_enrollment_trial_state(
            cast(EnrollmentTrial, trial)
        ),
    }
