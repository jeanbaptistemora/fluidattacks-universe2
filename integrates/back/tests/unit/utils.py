from dataloaders import (
    apply_context_attrs,
)
from datetime import (
    datetime,
    timedelta,
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
    request = apply_context_attrs(request)
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
    payload = {
        "user_email": username,
        "first_name": "unit",
        "last_name": "test",
        "exp": datetime.utcnow() + timedelta(seconds=SESSION_COOKIE_AGE),
        "sub": "starlette_session",
        "jti": token_utils.calculate_hash_token()["jti"],
    }
    token = token_utils.new_encoded_jwt(payload)
    if session_jwt:
        request.headers["Authorization"] = f"Bearer {session_jwt}"
    else:
        request.cookies[JWT_COOKIE_NAME] = token
        await redis_set_entity_attr(
            entity="session",
            attr="jti",
            email=payload["user_email"],
            value=payload["jti"],
            ttl=SESSION_COOKIE_AGE,
        )
        await redis_set_entity_attr(
            entity="session",
            attr="jwt",
            email=payload["user_email"],
            value=token,
            ttl=SESSION_COOKIE_AGE,
        )

    return request


def create_dummy_info(request: Request) -> GraphQLResolveInfo:
    return GraphQLResolveInfo(
        field_name=None,
        field_nodes=None,
        return_type=None,
        parent_type=None,
        path=None,
        schema=None,
        fragments=None,
        root_value=None,
        operation=None,
        variable_values=None,
        context=request,
        is_awaitable=None,
    )
