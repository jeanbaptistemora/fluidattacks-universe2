# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from db_model import (
    TABLE,
)
from dynamodb.types import (
    Facet,
)

ALL_SUBSCRIPTIONS_INDEX_METADATA = Facet(
    attrs=TABLE.facets["stakeholder_subscription"].attrs,
    pk_alias="SUBS#all",
    sk_alias="SUBS#frequency",
)

SUBSCRIPTIONS_PREFIX = "SUBS#"
