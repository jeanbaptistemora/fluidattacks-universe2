from typing import (
    Dict,
)

SINGLE_JOBS = frozenset(
    [
        "announcekit",
        "bugsnag",
        "checkly",
        "compute_bills",
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
        "code_upload",
    ]
)

COMPOUND_JOBS_TABLES: Dict[str, str] = {
    "dynamo": "dynamo_tables",
    "mirror": "last_sync_date",
}
