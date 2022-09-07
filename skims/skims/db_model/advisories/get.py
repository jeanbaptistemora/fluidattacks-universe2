# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from .types import (
    Advisory,
)
from .utils import (
    format_item_to_advisory,
)
from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
)
from boto3.dynamodb.conditions import (
    Key,
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
    Tuple,
)


async def _get_advisories(
    *, platform: str, package_name: str
) -> Tuple[Advisory, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets["advisories"],
        values={"platform": platform, "pkg_name": package_name},
    )

    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
        ),
        facets=(TABLE.facets["advisories"],),
        table=TABLE,
    )

    return tuple(format_item_to_advisory(item) for item in response.items)


class AdvisoriesLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, ad_keys: Iterable[Tuple[str, str]]
    ) -> Tuple[Advisory, ...]:
        return await collect(
            tuple(
                _get_advisories(platform=platform, package_name=package_name)
                for platform, package_name in ad_keys
            )
        )
