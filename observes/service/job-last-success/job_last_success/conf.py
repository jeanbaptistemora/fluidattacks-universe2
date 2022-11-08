# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from typing import (
    Dict,
)

SINGLE_JOBS = frozenset(
    [
        "announcekit",
        "bugsnag",
        "checkly",
        "new_checkly",
        "delighted",
        "formstack",
        "mailchimp",
        "matomo",
        "mixpanel_integrates",
        "timedoctor_backup",
        "timedoctor_etl",
        "timedoctor_refresh_token",
        "zoho_crm_etl",
        "zoho_crm_prepare",
    ]
)

COMPOUND_JOBS = frozenset(
    [
        "dynamo",
        "mirror",
    ]
)

COMPOUND_JOBS_TABLES: Dict[str, str] = {
    "dynamo": "dynamo_tables",
    "mirror": "last_sync_date",
}
