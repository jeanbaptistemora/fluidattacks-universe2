from .types import (
    Enrollment,
)
from db_model import (
    TABLE,
)
from db_model.utils import (
    serialize,
)
from dynamodb import (
    keys,
    operations,
)
import simplejson as json


async def add(*, enrollment: Enrollment) -> None:
    enrollment = enrollment._replace(email=enrollment.email.lower().strip())
    key_structure = TABLE.primary_key
    enrollment_key = keys.build_key(
        facet=TABLE.facets["enrollment_metadata"],
        values={"email": enrollment.email},
    )
    item = await operations.get_item(
        facets=(TABLE.facets["enrollment_metadata"],),
        key=enrollment_key,
        table=TABLE,
    )

    if not item:
        item = {
            key_structure.partition_key: enrollment_key.partition_key,
            key_structure.sort_key: enrollment_key.sort_key,
            **json.loads(json.dumps(enrollment, default=serialize)),
        }
    else:
        item["enrolled"] = True

    await operations.put_item(
        facet=TABLE.facets["enrollment_metadata"],
        item=item,
        table=TABLE,
    )
