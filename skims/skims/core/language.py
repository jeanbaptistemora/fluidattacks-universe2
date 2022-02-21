from integrates.dal import (
    get_group_language,
)
from integrates.graphql import (
    create_session,
)
from model.core_model import (
    LocalesEnum,
)
import sys


async def main(group: str, token: str) -> bool:
    success: bool = True

    create_session(api_token=token)

    locale: LocalesEnum = (await get_group_language(group)) or LocalesEnum.EN
    sys.stdout.write(locale.value)
    sys.stdout.write("\n")

    return success
