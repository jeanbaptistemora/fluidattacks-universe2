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
from newutils import (
    token as token_utils,
)
from stakeholders import (
    domain as stakeholders_domain,
)


@convert_kwargs_to_snake_case
async def mutate(
    _: None, info: GraphQLResolveInfo, token: str
) -> SimplePayloadType:
    user_info = await token_utils.get_jwt_content(info.context)
    user_email = user_info["user_email"]
    await stakeholders_domain.add_push_token(
        info.context.loaders, user_email, token
    )

    return SimplePayloadType(success=True)
