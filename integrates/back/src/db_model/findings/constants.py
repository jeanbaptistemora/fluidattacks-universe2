# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from db_model import (
    TABLE,
)
from dynamodb.types import (
    Facet,
)

ME_DRAFTS_INDEX_METADATA = Facet(
    attrs=TABLE.facets["finding_metadata"].attrs,
    pk_alias="USER#email",
    sk_alias="FIN#id",
)
