from authlib.integrations.starlette_client import (
    OAuth,
    OAuthError,
)
from datetime import (
    datetime,
    timedelta,
)
from decorators import (
    retry_on_exceptions,
)
from newutils import (
    token as token_utils,
)
from redis_cluster.operations import (
    redis_set_entity_attr,
)
from settings import (
    JWT_COOKIE_NAME,
    JWT_COOKIE_SAMESITE,
    SESSION_COOKIE_AGE,
)
from starlette.requests import (
    Request,
)
from starlette.responses import (
    HTMLResponse,
)
from typing import (
    Any,
    Dict,
)


async def create_session_token(user: Dict[str, str]) -> str:
    jti = token_utils.calculate_hash_token()["jti"]
    user_email = user["username"]
    jwt_token: str = token_utils.new_encoded_jwt(
        dict(
            user_email=user_email,
            first_name=user["first_name"],
            last_name=user["last_name"],
            exp=datetime.utcnow() + timedelta(seconds=SESSION_COOKIE_AGE),
            sub="starlette_session",
            jti=jti,
        )
    )

    await redis_set_entity_attr(
        entity="session",
        attr="jti",
        email=user_email,
        value=jti,
        ttl=SESSION_COOKIE_AGE,
    )
    await redis_set_entity_attr(
        entity="session",
        attr="jwt",
        email=user_email,
        value=jwt_token,
        ttl=SESSION_COOKIE_AGE,
    )
    return jwt_token


async def get_bitbucket_oauth_userinfo(
    client: OAuth, token: Dict[str, str]
) -> Dict[str, str]:
    query_headers = {"Authorization": f'Bearer {token["access_token"]}'}
    user = await client.get("user", token=token, headers=query_headers)
    emails = await client.get(
        "user/emails", token=token, headers=query_headers
    )

    user_name = user.json().get("display_name", "")
    email = next(
        iter(
            [
                email.get("email", "")
                for email in emails.json().get("values", "")
                if email.get("is_primary")
            ]
        ),
        "",
    )
    return {
        "email": email,
        "given_name": user_name.split(" ")[0],
        "family_name": user_name.split(" ")[1] if len(user_name) == 2 else "",
    }


@retry_on_exceptions(
    exceptions=(OAuthError,),
    max_attempts=5,
    sleep_seconds=float("0.5"),
)
async def get_jwt_userinfo(
    client: OAuth, request: Request, token: str
) -> Dict[str, str]:
    return dict(
        await client.parse_id_token(
            request,
            token,
            # Workaround to support microsoft multi-tenant
            claims_options={} if client.name == "azure" else None,
        )
    )


def get_redirect_url(request: Request, pattern: str) -> Any:
    return request.url_for(pattern).replace("http:", "https:")


def set_token_in_response(response: HTMLResponse, token: str) -> HTMLResponse:
    response.set_cookie(
        key=JWT_COOKIE_NAME,
        samesite=JWT_COOKIE_SAMESITE,
        value=token,
        secure=True,
        httponly=True,
        max_age=SESSION_COOKIE_AGE,
    )
    return response
