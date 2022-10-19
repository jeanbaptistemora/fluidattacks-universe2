# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from dataloaders import (
    apply_context_attrs,
)
from datetime import (
    datetime,
    timedelta,
)
from db_model import (
    stakeholders as stakeholders_model,
)
from db_model.stakeholders.types import (
    StakeholderMetadataToUpdate,
    StakeholderSessionToken,
    StateSessionType,
)
from graphql import (
    GraphQLResolveInfo,
)
from newutils import (
    token as token_utils,
)
from redis_cluster.operations import (
    redis_set_entity_attr,
)
from requests import (
    Request,
)
from settings import (
    JWT_COOKIE_NAME,
    SESSION_COOKIE_AGE,
)
from typing import (
    Optional,
)
import uuid


def create_dummy_simple_session(
    username: str = "unittest",
) -> Request:
    request = Request("GET", "/")
    request = apply_context_attrs(request)  # type: ignore
    setattr(
        request,
        "session",
        dict(username=username, session_key=str(uuid.uuid4())),
    )
    setattr(request, "cookies", {})

    return request


async def create_dummy_session(
    username: str = "unittest", session_jwt: Optional[str] = None
) -> Request:
    request = create_dummy_simple_session(username)
    jti = token_utils.calculate_hash_token()["jti"]
    expiration_time = int(
        (datetime.utcnow() + timedelta(seconds=SESSION_COOKIE_AGE)).timestamp()
    )
    payload = {
        "user_email": username,
        "first_name": "unit",
        "last_name": "test",
        "jti": jti,
    }
    token = token_utils.encode_token(
        expiration_time=expiration_time,
        payload=payload,
        subject="starlette_session",
    )
    if session_jwt:
        request.headers["Authorization"] = f"Bearer {session_jwt}"
    else:
        request.cookies[JWT_COOKIE_NAME] = token
        # do not use me query to validate if an stakeholder
        # has been removed because update_metadata will create that user
        await stakeholders_model.update_metadata(
            email=username,
            metadata=StakeholderMetadataToUpdate(
                session_token=StakeholderSessionToken(
                    jti=jti, state=StateSessionType.IS_VALID
                )
            ),
        )

        await redis_set_entity_attr(
            entity="session",
            attr="jti",
            email=username,
            value=payload["jti"],
            ttl=SESSION_COOKIE_AGE,
        )
        await redis_set_entity_attr(
            entity="session",
            attr="jwt",
            email=username,
            value=token,
            ttl=SESSION_COOKIE_AGE,
        )

    return request


def create_dummy_info(request: Request) -> GraphQLResolveInfo:
    return GraphQLResolveInfo(
        field_name=None,  # type: ignore
        field_nodes=None,  # type: ignore
        return_type=None,  # type: ignore
        parent_type=None,  # type: ignore
        path=None,  # type: ignore
        schema=None,  # type: ignore
        fragments=None,  # type: ignore
        root_value=None,
        operation=None,  # type: ignore
        variable_values=None,  # type: ignore
        context=request,
        is_awaitable=None,  # type: ignore
    )
