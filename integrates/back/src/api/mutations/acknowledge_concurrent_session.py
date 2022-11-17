# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from api.mutations import (
    SimplePayload as SimplePayloadType,
)
from ariadne import (
    convert_kwargs_to_snake_case,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from sessions import (
    domain as sessions_domain,
)
from stakeholders import (
    domain as stakeholders_domain,
)


@convert_kwargs_to_snake_case
async def mutate(
    _: None,
    info: GraphQLResolveInfo,
) -> SimplePayloadType:
    user_info = await sessions_domain.get_jwt_content(info.context)
    user_email = user_info["user_email"]
    await stakeholders_domain.acknowledge_concurrent_session(user_email)

    return SimplePayloadType(success=True)
