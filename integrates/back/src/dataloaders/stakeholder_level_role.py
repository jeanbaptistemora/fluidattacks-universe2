from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
)
import authz


class StakeholderLevelRoleLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(self, emails: tuple[str, ...]) -> tuple[str, ...]:
        return await collect(
            tuple(authz.get_user_level_role(email) for email in emails)
        )
