from enum import (
    Enum,
)
from fa_purity.frozen import (
    FrozenDict,
    FrozenList,
)
from jobs_scheduler.cron.core import (
    AnyTime,
    Cron,
    CronItem,
)
from jobs_scheduler.cron.factory import (
    week_days,
    weekly,
    work_days,
)
import os
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
        return Success(Jobs[raw.upper()])
    except KeyError:
        return Failure(InvalidJob())


def behind_work_days(minute: CronItem, hour: CronItem) -> Cron:
    return week_days(minute, hour, range(0, 5)).unwrap()  # Sun - Thu


ANY = AnyTime()
SCHEDULE: FrozenDict[Cron, FrozenList[Jobs]] = FrozenDict(
    {
        work_days(ANY, ANY).unwrap(): (Jobs.REPORT_FAILS,),
        behind_work_days(ANY, 22): (Jobs.DYNAMO_INTEGRATES_MAIN,),
        behind_work_days(ANY, 23): (Jobs.MAILCHIMP_ETL,),
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
