# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from __future__ import (
    annotations,
)

from enum import (
    Enum,
)
from fa_purity import (
    Result,
)


class InvalidJob(Exception):
    pass


class Job(Enum):
    ANNOUNCEKIT = "ANNOUNCEKIT"
    BUGSNAG = "BUGSNAG"
    CHECKLY = "CHECKLY"
    CHECKLY_LEGACY = "CHECKLY_LEGACY"
    DELIGHTED = "DELIGHTED"
    DYNAMO_FORCES = "DYNAMO_FORCES"
    DYNAMO_INTEGRATES = "DYNAMO_INTEGRATES"
    DYNAMO_INTEGRATES_MAIN = "DYNAMO_INTEGRATES_MAIN"
    DYNAMO_INTEGRATES_MAIN_NO_CACHE = "DYNAMO_INTEGRATES_MAIN_NO_CACHE"
    FORMSTACK = "FORMSTACK"
    GITLAB_PRODUCT = "GITLAB_PRODUCT"
    GITLAB_CHALLENGES = "GITLAB_CHALLENGES"
    GITLAB_DEFAULT = "GITLAB_DEFAULT"
    GITLAB_SERVICES = "GITLAB_SERVICES"
    MAILCHIMP_ETL = "MAILCHIMP_ETL"
    MANDRILL_ETL = "MANDRILL_ETL"
    MIRROR = "MIRROR"
    REPORT_FAILS = "REPORT_FAILS"
    REPORT_CANCELLED = "REPORT_CANCELLED"
    UPLOAD = "UPLOAD"

    @staticmethod
    def new_job(raw: str) -> Result[Job, InvalidJob]:
        try:
            return Result.success(Job[raw.upper()])
        except KeyError:
            return Result.failure(InvalidJob())
