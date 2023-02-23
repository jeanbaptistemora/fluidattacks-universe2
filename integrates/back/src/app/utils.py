from authlib.integrations.starlette_client import (
    OAuth,
    OAuthError,
)
from decorators import (
    retry_on_exceptions,
)
from httpx import (
    ConnectTimeout,
)
from starlette.requests import (
    Request,
)
from typing import (
    Any,
)


async def get_bitbucket_oauth_userinfo(
    client: OAuth, token: dict[str, str]
) -> dict[str, str]:
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
    exceptions=(ConnectTimeout, OAuthError),
    max_attempts=5,
    sleep_seconds=float("0.5"),
)
async def get_jwt_userinfo(
    client: OAuth, request: Request, token: str
) -> dict[str, str]:
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
