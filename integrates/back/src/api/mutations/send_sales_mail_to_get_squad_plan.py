from .payloads.types import (
    SimplePayload,
)
from dataloaders import (
    Dataloaders,
)
from db_model.stakeholders.types import (
    StakeholderPhone,
)
from decorators import (
    concurrent_decorators,
    require_corporate_email,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from mailer import (
    forms as forms_mail,
)
from typing import (
    Dict,
)


@concurrent_decorators(
    require_corporate_email,
    require_login,
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    name: str,
    email: str,
    phone: Dict[str, str],
) -> SimplePayload:

    loaders: Dataloaders = info.context.loaders
    await forms_mail.send_mail_to_get_squad_plan(
        loaders=loaders,
        name=name,
        email=email,
        phone=StakeholderPhone(
            national_number=phone["nationalNumber"],
            calling_country_code=phone["callingCountryCode"],
            country_code="",
        ),
    )

    return SimplePayload(success=True)
