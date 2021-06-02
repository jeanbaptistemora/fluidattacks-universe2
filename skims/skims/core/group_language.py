from integrates.dal import (
    get_group_language,
)
from integrates.graphql import (
    create_session,
)
import sys


async def main(group: str, token: str) -> bool:
    success: bool = True

    create_session(api_token=token)

    language: str = await get_group_language(group=group)
    sys.stdout.write(language)
    sys.stdout.write("\n")

    return success
