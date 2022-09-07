# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from db_model import (
    TABLE,
)
from dynamodb.types import (
    Facet,
)

ORGANIZATION_ID_PREFIX = "ORG#"


ALL_ORGANIZATIONS_INDEX_METADATA = Facet(
    attrs=TABLE.facets["organization_metadata"].attrs,
    pk_alias="ORG#all",
    sk_alias="ORG#id",
)
