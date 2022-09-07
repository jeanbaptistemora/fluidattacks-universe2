# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from .types import (
    Enrollment,
)
from db_model import (
    TABLE,
)
from dynamodb import (
    keys,
    operations,
)
import simplejson as json  # type: ignore


async def add(*, enrollment: Enrollment) -> None:
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
            **json.loads(json.dumps(enrollment)),
        }
    else:
        item["enrolled"] = True

    await operations.put_item(
        facet=TABLE.facets["enrollment_metadata"],
        item=item,
        table=TABLE,
    )
