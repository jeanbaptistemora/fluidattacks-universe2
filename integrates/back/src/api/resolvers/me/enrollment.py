from dataloaders import (
    Dataloaders,
)
from db_model.enrollment.types import (
    Enrollment,
)
from db_model.stakeholders.types import (
    Stakeholder,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Any,
    Dict,
)


async def resolve(
    parent: Dict[str, Any], info: GraphQLResolveInfo, **_kwargs: None
) -> Enrollment:
    user_email = str(parent["user_email"])
    loaders: Dataloaders = info.context.loaders
    enrollment: Enrollment = await loaders.enrollment.load(user_email)
    stakeholder: Stakeholder = await loaders.stakeholder.load(user_email)

    if stakeholder.enrolled:
        return Enrollment(
            email=stakeholder.email, enrolled=stakeholder.enrolled
        )
    return enrollment
