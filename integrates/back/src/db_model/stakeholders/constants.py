# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from db_model import (
    TABLE,
)
from dynamodb.types import (
    Facet,
)

ALL_STAKEHOLDERS_INDEX_METADATA = Facet(
    attrs=TABLE.facets["stakeholder_metadata"].attrs,
    pk_alias="USER#all",
    sk_alias="USER#email",
)
