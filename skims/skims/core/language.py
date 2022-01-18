from integrates.dal import (
    get_group_language,
)
from integrates.graphql import (
    create_session,
)
from model import (
    core_model,
)
import sys


async def main(group: str, token: str) -> bool:
    success: bool = True

    create_session(api_token=token)

    locale: core_model.LocalesEnum = (
        await get_group_language(group)
    ) or core_model.LocalesEnum.EN
    sys.stdout.write(locale.value)
    sys.stdout.write("\n")

    return success
