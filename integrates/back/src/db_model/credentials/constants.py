# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from db_model import (
    TABLE,
)
from dynamodb.types import (
    Facet,
)

OWNER_INDEX_FACET = Facet(
    attrs=TABLE.facets["credentials_metadata"].attrs,
    pk_alias="OWNER#owner",
    sk_alias="CRED#id",
)
