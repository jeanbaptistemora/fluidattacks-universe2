# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from redshift.operations import (
    SCHEMA_NAME,
)

METADATA_TABLE: str = f"{SCHEMA_NAME}.events_metadata"
