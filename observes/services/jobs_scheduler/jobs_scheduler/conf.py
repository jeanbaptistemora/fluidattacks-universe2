# pylint: skip-file

from enum import (
    Enum,
)
from jobs_scheduler.cron_2.core import (
    AnyTime,
    Cron,
    CronDraft,
)
from jobs_scheduler.cron_2.factory import (
    new as new_cron,
    week_days,
    weekly,
    work_days,
)
import os
from purity.v2.frozen import (
    FrozenDict,
    FrozenList,
)
from returns.result import (
    Failure,
    Result,
    Success,
)


class InvalidJob(Exception):
    pass


class Jobs(Enum):
    ANNOUNCEKIT = os.environ["announceKitEtl"]
    BUGSNAG = os.environ["bugsnagEtl"]
    CHECKLY = os.environ["checklyEtl"]
    DELIGHTED = os.environ["delightedEtl"]
    DYNAMO_FORCES = f'{os.environ["dynamoDbEtls"]} FORCES'
    DYNAMO_INTEGRATES = f'{os.environ["dynamoDbEtls"]} GROUP'
    DYNAMO_INTEGRATES_MAIN = f'{os.environ["dynamoDbEtls"]} CORE'
    FORMSTACK = os.environ["formstackEtl"]
    GITLAB_PRODUCT = os.environ["gitlabEtlProduct"]
    GITLAB_CHALLENGES = os.environ["gitlabEtlChallenges"]
    GITLAB_DEFAULT = os.environ["gitlabEtlDefault"]
    GITLAB_SERVICES = os.environ["gitlabEtlServices"]
    MAILCHIMP_ETL = os.environ["mailchimpEtl"]
    MIRROR = os.environ["codeEtlMirror"]
    REPORT_FAILS = os.environ["batchStability"] + " report-failures observes"
    REPORT_CANCELLED = (
        os.environ["batchStability"] + " report-cancelled observes"
    )
    UPLOAD = os.environ["codeEtlUpload"]


def new_job(raw: str) -> Result[Jobs, InvalidJob]:
    try:
        return Success(Jobs[raw])
    except KeyError:
        return Failure(InvalidJob())


ANY = AnyTime()
SCHEDULE: FrozenDict[Cron, FrozenList[Jobs]] = FrozenDict(
    {
        new_cron(CronDraft(ANY, 18, 16, 3, ANY)).unwrap(): (
            Jobs.MAILCHIMP_ETL,
        ),
        work_days(ANY, ANY).unwrap(): (Jobs.REPORT_FAILS,),
        week_days(ANY, 22, range(0, 5)).unwrap(): (
            Jobs.DYNAMO_INTEGRATES_MAIN,
        ),
        work_days(ANY, 0).unwrap(): (
            Jobs.MIRROR,
            Jobs.REPORT_CANCELLED,
        ),
        weekly(ANY, 3, 1).unwrap(): (
            Jobs.ANNOUNCEKIT,
            Jobs.BUGSNAG,
            Jobs.CHECKLY,
            Jobs.DELIGHTED,
        ),
        work_days(ANY, 6).unwrap(): (Jobs.UPLOAD,),
        work_days(ANY, range(7, 19, 2)).unwrap(): (
            Jobs.GITLAB_PRODUCT,
            Jobs.GITLAB_CHALLENGES,
            Jobs.GITLAB_DEFAULT,
            Jobs.GITLAB_SERVICES,
        ),
        work_days(ANY, (11, 18)).unwrap(): (Jobs.FORMSTACK,),
        work_days(ANY, range(0, 16, 5)).unwrap(): (Jobs.DYNAMO_FORCES,),
        work_days(ANY, range(5, 19, 3)).unwrap(): (Jobs.DYNAMO_INTEGRATES,),
    }
)
