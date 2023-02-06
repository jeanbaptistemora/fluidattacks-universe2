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
    DELIGHTED = "DELIGHTED"
    DYNAMO_INTEGRATES_MAIN = "DYNAMO_INTEGRATES_MAIN"
    DYNAMO_INTEGRATES_MAIN_NO_CACHE = "DYNAMO_INTEGRATES_MAIN_NO_CACHE"
    FORMSTACK = "FORMSTACK"
    GITLAB_PRODUCT = "GITLAB_PRODUCT"
    MAILCHIMP_ETL = "MAILCHIMP_ETL"
    MANDRILL_ETL = "MANDRILL_ETL"
    MIRROR = "MIRROR"
    UPLOAD = "UPLOAD"

    @staticmethod
    def new_job(raw: str) -> Result[Job, InvalidJob]:
        try:
            return Result.success(Job[raw.upper()])
        except KeyError:
            return Result.failure(InvalidJob())
