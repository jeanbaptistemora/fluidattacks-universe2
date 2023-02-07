from fa_purity.frozen import (
    FrozenDict,
    FrozenList,
)
from jobs_scheduler.conf.job import (
    Job,
)
from jobs_scheduler.cron.core import (
    Cron,
    CronItem,
    Days,
    DaysRange,
)
from jobs_scheduler.cron.factory import (
    behind_work_days,
    weekly,
    work_days,
)

ANY = CronItem.any()
SCHEDULE: FrozenDict[Cron, FrozenList[Job]] = FrozenDict(
    {
        weekly(ANY, 0, frozenset([Days.SAT])).unwrap(): (
            Job.DYNAMO_INTEGRATES_MAIN_NO_CACHE,
        ),
        behind_work_days(ANY, 23): (Job.MAILCHIMP_ETL, Job.MANDRILL_ETL),
        work_days(ANY, 0).unwrap(): (
            Job.DYNAMO_INTEGRATES_MAIN,
            Job.MIRROR,
        ),
        weekly(ANY, 3, DaysRange.new(Days.MON, Days.FRI).unwrap()).unwrap(): (
            Job.ANNOUNCEKIT,
            Job.BUGSNAG,
            Job.CHECKLY,
            Job.DELIGHTED,
        ),
        work_days(ANY, 6).unwrap(): (Job.UPLOAD,),
        work_days(ANY, CronItem.from_range(range(7, 19, 4))).unwrap(): (
            Job.GITLAB_PRODUCT,
        ),
        weekly(
            ANY,
            CronItem.from_range(range(7, 19, 3)),
            frozenset([Days.SAT, Days.SUN]),
        ).unwrap(): (Job.GITLAB_PRODUCT,),
        work_days(ANY, CronItem.from_values(frozenset([11, 18]))).unwrap(): (
            Job.FORMSTACK,
        ),
        weekly(
            ANY,
            CronItem.from_values(frozenset([0, 11])),
            frozenset([Days.SUN]),
        ).unwrap(): (Job.FORMSTACK,),
    }
)
