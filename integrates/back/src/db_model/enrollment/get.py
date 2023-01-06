from .types import (
    Enrollment,
)
from .utils import (
    format_enrollment,
)
from aiodataloader import (
    DataLoader,
)
from db_model import (
    TABLE,
)
from dynamodb import (
    keys,
    operations,
)
from typing import (
    Iterable,
)


async def _get_enrollments(*, emails: Iterable[str]) -> tuple[Enrollment, ...]:
    emails = tuple(email.lower().strip() for email in emails)
    primary_keys = tuple(
        keys.build_key(
            facet=TABLE.facets["enrollment_metadata"],
            values={"email": email},
        )
        for email in emails
    )
    items = await operations.batch_get_item(keys=primary_keys, table=TABLE)

    enrollments: list[Enrollment] = []
    for email in emails:
        enrollment: Enrollment = next(
            (
                format_enrollment(item)
                for item in items
                if item.get("email") == email
            ),
            Enrollment(  # Fallback for this entity
                email=email,
                enrolled=False,
            ),
        )
        enrollments.append(enrollment)

    return tuple(enrollments)


class EnrollmentLoader(DataLoader):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, emails: Iterable[str]
    ) -> tuple[Enrollment, ...]:
        return await _get_enrollments(emails=tuple(emails))
