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


async def _get_enrollments(*, emails: Iterable[str]) -> list[Enrollment]:
    emails = [email.lower().strip() for email in emails]
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

    return enrollments


class EnrollmentLoader(DataLoader[str, Enrollment]):
    # pylint: disable=method-hidden
    async def batch_load_fn(self, emails: Iterable[str]) -> list[Enrollment]:
        return await _get_enrollments(emails=emails)
