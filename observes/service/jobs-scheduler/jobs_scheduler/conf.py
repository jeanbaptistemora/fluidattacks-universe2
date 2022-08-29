from enum import (
    Enum,
)
from fa_purity.frozen import (
    FrozenDict,
    FrozenList,
)
from fa_purity.result import (
    Result,
)
from jobs_scheduler.cron.core import (
    AnyTime,
    Cron,
    CronItem,
    Days,
    DaysRange,
)
from jobs_scheduler.cron.factory import (
    week_days,
    weekly,
    work_days,
)
import os


class InvalidJob(Exception):
    pass


class Jobs(Enum):
    ANNOUNCEKIT = os.environ.get("announceKitEtl", "")
    BUGSNAG = os.environ.get("bugsnagEtl", "")
    CHECKLY = os.environ.get("checklyEtl", "")
    DELIGHTED = os.environ.get("delightedEtl", "")
    DYNAMO_FORCES = f'{os.environ.get("dynamoDbEtls", "")} FORCES'
    DYNAMO_INTEGRATES = f'{os.environ.get("dynamoDbEtls", "")} GROUP'
    DYNAMO_INTEGRATES_MAIN = f'{os.environ.get("dynamoDbEtls", "")} CORE'
    DYNAMO_INTEGRATES_MAIN_NO_CACHE = (
        f'{os.environ.get("dynamoDbEtls", "")} CORE_NO_CACHE'
    )
    FORMSTACK = os.environ.get("formstackEtl", "")
    GITLAB_PRODUCT = os.environ.get("gitlabEtlProduct", "")
    GITLAB_CHALLENGES = os.environ.get("gitlabEtlChallenges", "")
    GITLAB_DEFAULT = os.environ.get("gitlabEtlDefault", "")
    GITLAB_SERVICES = os.environ.get("gitlabEtlServices", "")
    MAILCHIMP_ETL = os.environ.get("mailchimpEtl", "")
    MANDRILL_ETL = os.environ.get("mandrillEtl", "")
    MIRROR = os.environ.get("codeEtlMirror", "")
    REPORT_FAILS = (
        os.environ.get("batchStability", "") + " report-failures observes"
    )
    REPORT_CANCELLED = (
        os.environ.get("batchStability", "") + " report-cancelled observes"
    )
    UPLOAD = os.environ.get("codeEtlUpload", "")


def new_job(raw: str) -> Result[Jobs, InvalidJob]:
    try:
        return Result.success(Jobs[raw.upper()])
    except KeyError:
        return Result.failure(InvalidJob())


def behind_work_days(minute: CronItem, hour: CronItem) -> Cron:
    return week_days(minute, hour, DaysRange(Days.SUN, Days.THU)).unwrap()


ANY = AnyTime()
SCHEDULE: FrozenDict[Cron, FrozenList[Jobs]] = FrozenDict(
    {
        work_days(ANY, ANY).unwrap(): (Jobs.REPORT_FAILS,),
        weekly(ANY, 0, 6).unwrap(): (Jobs.DYNAMO_INTEGRATES_MAIN_NO_CACHE,),
        work_days(ANY, 3).unwrap(): (Jobs.DYNAMO_INTEGRATES_MAIN,),
        behind_work_days(ANY, 23): (Jobs.MAILCHIMP_ETL, Jobs.MANDRILL_ETL),
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
        week_days(
            ANY, range(0, 16, 5), DaysRange(Days.MON, Days.SAT)
        ).unwrap(): (Jobs.DYNAMO_FORCES,),
        week_days(
            ANY, range(5, 19, 3), DaysRange(Days.MON, Days.SAT)
        ).unwrap(): (Jobs.DYNAMO_INTEGRATES,),
    }
)
