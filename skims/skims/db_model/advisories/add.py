# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from .types import (
    Advisory,
)
from .update import (
    update,
)
from boto3.dynamodb.conditions import (
    Key,
)
from custom_exceptions import (
    AdvisoryAlreadyCreated,
    InvalidSeverity,
    InvalidVulnerableVersion,
)
from db_model import (
    TABLE,
)
from db_model.advisories.utils import (
    format_advisory,
)
from dynamodb import (
    keys,
    operations,
)
import simplejson as json
from typing import (
    List,
    Optional,
)
from utils.logs import (
    log_blocking,
)


async def add(
    *,
    advisory: Advisory,
    no_overwrite: bool = False,
    to_storage: Optional[List[Advisory]] = None,
) -> None:
    try:
        await _add(advisory=advisory, no_overwrite=no_overwrite)
        if to_storage is not None:
            to_storage.append(advisory)
    except (
        AdvisoryAlreadyCreated,
        InvalidSeverity,
        InvalidVulnerableVersion,
    ) as exc:
        log_blocking(
            "warning",
            "Advisory SOURCE#%s#ADVISORY#%s wasn't added. %s",
            advisory.source,
            advisory.associated_advisory,
            exc.new(),
        )


async def _add(*, advisory: Advisory, no_overwrite: bool) -> None:
    advisory = format_advisory(advisory)
    items = []
    key_structure = TABLE.primary_key
    advisory_key = keys.build_key(
        facet=TABLE.facets["advisories"],
        values={
            "platform": advisory.package_manager,
            "pkg_name": advisory.package_name,
            "src": advisory.source,
            "id": advisory.associated_advisory,
        },
    )

    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(advisory_key.partition_key)
            & Key(key_structure.sort_key).eq(advisory_key.sort_key)
        ),
        facets=(TABLE.facets["advisories"],),
        limit=1,
        table=TABLE,
    )
    if response.items:
        if no_overwrite:
            raise AdvisoryAlreadyCreated()
        current_ad = response.items[0]
        if (
            current_ad.get("vulnerable_version") != advisory.vulnerable_version
            or current_ad.get("severity") != advisory.severity
        ):
            advisory = advisory._replace(
                created_at=current_ad.get("created_at")
            )
            await update(advisory=advisory, checked=True)
    else:
        advisory_item = {
            key_structure.partition_key: advisory_key.partition_key,
            key_structure.sort_key: advisory_key.sort_key,
            **json.loads(json.dumps(advisory)),
        }
        items.append(advisory_item)

        await operations.batch_put_item(items=tuple(items), table=TABLE)
        print(f"Added ( {advisory_key.sort_key} )")
