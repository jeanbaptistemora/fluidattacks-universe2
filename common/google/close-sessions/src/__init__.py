from google.oauth2.service_account import (
    Credentials,
)
from googleapiclient.discovery import (
    build,
)
import json
import os
from typing import (
    Any,
)

API: Any = build(
    "admin",
    "directory_v1",
    credentials=Credentials.from_service_account_info(
        json.loads(os.environ["GOOGLE_AUTH"]),
        scopes=[
            "https://www.googleapis.com/auth/admin.directory.user",
            "https://www.googleapis.com/auth/admin.directory.user.security",
        ],
        subject="jrestrepo@fluidattacks.com",
    ),
)

BROWSER_TOKENS: set[str] = {
    "Google Chrome",
}


def get_user_emails() -> list[str]:
    result: Any = (
        API.users()
        .list(
            customer="my_customer",
            maxResults=500,
        )
        .execute()
    )

    return [user["primaryEmail"] for user in result.get("users", [])]


def get_browser_tokens() -> list[dict[str, str]]:
    browser_tokens: list[dict[str, str]] = []
    for email in get_user_emails():
        result: Any = API.tokens().list(userKey=email).execute()
        browser_tokens.extend(
            [
                {
                    "userKey": email,
                    "clientId": token["clientId"],
                }
                for token in result.get("items", [])
                if token["displayText"] in BROWSER_TOKENS
            ]
        )

    return browser_tokens


def main() -> None:
    for token in get_browser_tokens():
        print(f'[INFO] Closing browser session for {token["userKey"]}')
        API.tokens().delete(
            userKey=token["userKey"],
            clientId=token["clientId"],
        ).execute()


main()
