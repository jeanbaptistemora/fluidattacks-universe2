# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from .types import (
    Advisory,
)
from .utils import (
    format_advisory,
    format_advisory_to_item,
)
from custom_exceptions import (
    InvalidSeverity,
    InvalidVulnerableVersion,
)
from db_model import (
    TABLE,
)
from dynamodb import (
    keys,
    operations,
)
from utils.logs import (
    log_blocking,
)


async def update(
    *,
    advisory: Advisory,
    checked: bool = False,
) -> None:
    try:
        await _update(advisory=advisory, checked=checked)
    except (
        InvalidSeverity,
        InvalidVulnerableVersion,
    ) as exc:
        log_blocking(
            "warning",
            "Advisory SOURCE#%s#ADVISORY#%s wasn't updated. %s",
            advisory.source,
            advisory.associated_advisory,
            exc.new(),
        )


async def _update(
    *,
    advisory: Advisory,
    checked: bool,
) -> None:
    advisory = format_advisory(
        advisory=advisory, is_update=True, checked=checked
    )
    advisory_key = keys.build_key(
        facet=TABLE.facets["advisories"],
        values={
            "platform": advisory.package_manager,
            "pkg_name": advisory.package_name,
            "src": advisory.source,
            "id": advisory.associated_advisory,
        },
    )
    advisory_item = format_advisory_to_item(advisory)
    await operations.update_item(
        item=advisory_item,
        key=advisory_key,
        table=TABLE,
    )
    print(f"Updated ( {advisory_key.sort_key} )")
