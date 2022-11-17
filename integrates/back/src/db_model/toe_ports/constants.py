# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from db_model import (
    TABLE,
)
from dynamodb.types import (
    Facet,
)

GSI_2_FACET = Facet(
    attrs=TABLE.facets["toe_port_metadata"].attrs,
    pk_alias="GROUP#group_name",
    sk_alias="PORTS#PRESENT#be_present#ROOT#root_id#ADDRESS#address#PORT#port",
)
