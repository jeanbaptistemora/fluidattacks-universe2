from dataloaders import (
    Dataloaders,
)
from db_model.companies.types import (
    Company,
    Trial,
)
from db_model.enrollment.types import (
    Enrollment,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Any,
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
            extension_date=None,
            extension_days=0,
            start_date=None,
        )
    )

    return {
        "completed": trial.completed,
        "extension_date": trial.extension_date or "",
        "extension_days": trial.extension_days,
        "start_date": trial.start_date or "",
        "state": "TRIAL",
    }
