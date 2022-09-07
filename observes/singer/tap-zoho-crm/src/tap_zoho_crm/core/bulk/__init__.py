# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from tap_zoho_crm.core.bulk.crud import (
    create_bulk_job,
    get_bulk_data,
    update_all,
)

__all__ = [
    "create_bulk_job",
    "update_all",
    "get_bulk_data",
]
