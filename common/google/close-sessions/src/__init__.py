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

CREDENTIALS = Credentials.from_service_account_info(
    json.loads(os.environ["GOOGLE_AUTH"]),
    scopes=["https://www.googleapis.com/auth/admin.directory.user"],
    subject="jrestrepo@fluidattacks.com",
)
SERVICE = build("admin", "directory_v1", credentials=CREDENTIALS)


def main() -> None:
    results: Any = (
        SERVICE.users()
        .list(
            customer="my_customer",
            maxResults=10,
            orderBy="email",
        )
        .execute()
    )
    print(results["users"])


main()
