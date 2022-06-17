from .types import (
    Enrollment,
    Trial,
)
from .utils import (
    format_enrollment,
)
from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
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


async def get_enrollment(*, email: str) -> Enrollment:
    email = email.lower().strip()
    primary_key = keys.build_key(
        facet=TABLE.facets["enrollment_metadata"],
        values={"email": email},
    )
    item = await operations.get_item(
        facets=(TABLE.facets["enrollment_metadata"],),
        key=primary_key,
        table=TABLE,
    )

    if not item:
        return Enrollment(
            email=email,
            enrolled=False,
            trial=Trial(
                completed=False,
                extension_date="",
                extension_days=0,
                start_date="",
            ),
        )

    return format_enrollment(item)


class EnrollmentLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, emails: Tuple[str, ...]
    ) -> Tuple[Enrollment, ...]:
        return await collect(
            tuple(get_enrollment(email=email) for email in emails)
        )
