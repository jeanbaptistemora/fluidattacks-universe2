# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from enum import (
    Enum,
)
from fa_purity.frozen import (
    FrozenDict,
    FrozenList,
)
from jobs_scheduler.conf.job import (
    Job,
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


def behind_work_days(minute: CronItem, hour: CronItem) -> Cron:
    return week_days(minute, hour, DaysRange(Days.SUN, Days.THU)).unwrap()


ANY = AnyTime()
SCHEDULE: FrozenDict[Cron, FrozenList[Job]] = FrozenDict(
    {
        work_days(ANY, ANY).unwrap(): (Job.REPORT_FAILS,),
        weekly(ANY, 0, 6).unwrap(): (Job.DYNAMO_INTEGRATES_MAIN_NO_CACHE,),
        work_days(ANY, 3).unwrap(): (Job.DYNAMO_INTEGRATES_MAIN,),
        behind_work_days(ANY, 23): (Job.MAILCHIMP_ETL, Job.MANDRILL_ETL),
        work_days(ANY, 0).unwrap(): (
            Job.MIRROR,
            Job.REPORT_CANCELLED,
        ),
        weekly(ANY, 3, 1).unwrap(): (
            Job.ANNOUNCEKIT,
            Job.BUGSNAG,
            Job.CHECKLY,
            Job.DELIGHTED,
        ),
        work_days(ANY, 6).unwrap(): (Job.UPLOAD,),
        work_days(ANY, range(7, 19, 1)).unwrap(): (
            Job.GITLAB_PRODUCT,
            Job.GITLAB_CHALLENGES,
            Job.GITLAB_DEFAULT,
            Job.GITLAB_SERVICES,
        ),
        work_days(ANY, (11, 18)).unwrap(): (Job.FORMSTACK,),
        week_days(
            ANY, range(0, 16, 5), DaysRange(Days.MON, Days.SAT)
        ).unwrap(): (Job.DYNAMO_FORCES,),
        week_days(
            ANY, range(5, 19, 3), DaysRange(Days.MON, Days.SAT)
        ).unwrap(): (Job.DYNAMO_INTEGRATES,),
    }
)
