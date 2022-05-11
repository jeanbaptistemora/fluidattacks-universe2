import asyncio
from okta.client import (
    Client,
)
import os
from typing import (
    Any,
)

CLIENT: Any = Client(
    {
        "orgUrl": "https://fluidattacks.okta.com",
        "token": os.environ["OKTA_API_TOKEN"],
        "raiseException": True,
    }
)


async def get_user_ids() -> list[str]:
    user_ids: list[str] = []
    users, resp, _ = await CLIENT.list_users(
        {
            "search": 'status eq "ACTIVE"',
            "limit": 50,
        }
    )
    while True:
        for user in users:
            user_ids.append(user.id)
        if resp.has_next():
            users, _ = await resp.next()
        else:
            break
    return user_ids


async def main() -> None:
    await get_user_ids()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
