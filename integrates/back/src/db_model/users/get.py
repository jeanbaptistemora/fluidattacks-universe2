from .types import (
    User,
)
from .utils import (
    format_user,
)
from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
)
from custom_exceptions import (
    UserNotFound,
)
from db_model import (
    TABLE,
)
from dynamodb import (
    keys,
    operations,
)
from typing import (
    Tuple,
)


async def _get_user(*, user_email: str) -> User:
    primary_key = keys.build_key(
        facet=TABLE.facets["user_metadata"],
        values={"email": user_email},
    )

    item = await operations.get_item(
        facets=(TABLE.facets["user_metadata"],),
        key=primary_key,
        table=TABLE,
    )

    if item:
        return format_user(item)

    raise UserNotFound()


class UserLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(self, emails: Tuple[str, ...]) -> Tuple[User, ...]:
        return await collect(
            tuple(_get_user(user_email=email) for email in emails)
        )
