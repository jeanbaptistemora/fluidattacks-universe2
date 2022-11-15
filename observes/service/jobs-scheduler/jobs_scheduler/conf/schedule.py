# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

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
        work_days(ANY, ANY).unwrap(): (Job.REPORT_FAILS,),
        weekly(ANY, 0, frozenset([Days.SAT])).unwrap(): (
            Job.DYNAMO_INTEGRATES_MAIN_NO_CACHE,
        ),
        work_days(ANY, 3).unwrap(): (Job.DYNAMO_INTEGRATES_MAIN,),
        behind_work_days(ANY, 23): (Job.MAILCHIMP_ETL, Job.MANDRILL_ETL),
        work_days(ANY, 0).unwrap(): (
            Job.MIRROR,
            Job.REPORT_CANCELLED,
        ),
        weekly(ANY, 3, DaysRange.new(Days.MON, Days.THU).unwrap()).unwrap(): (
            Job.ANNOUNCEKIT,
            Job.BUGSNAG,
            Job.CHECKLY,
            Job.CHECKLY_LEGACY,
            Job.DELIGHTED,
        ),
        work_days(ANY, 6).unwrap(): (Job.UPLOAD,),
        work_days(ANY, CronItem.from_range(range(7, 19, 1))).unwrap(): (
            Job.GITLAB_PRODUCT,
            Job.GITLAB_CHALLENGES,
            Job.GITLAB_DEFAULT,
            Job.GITLAB_SERVICES,
        ),
        work_days(ANY, CronItem.from_values(frozenset([11, 18]))).unwrap(): (
            Job.FORMSTACK,
        ),
        weekly(
            ANY,
            CronItem.from_values(frozenset([0, 11])),
            frozenset([Days.SUN]),
        ).unwrap(): (Job.FORMSTACK,),
        weekly(
            ANY,
            CronItem.from_range(range(0, 16, 5)),
            DaysRange.new(Days.MON, Days.SAT).unwrap(),
        ).unwrap(): (Job.DYNAMO_FORCES,),
        weekly(
            ANY,
            CronItem.from_range(range(5, 19, 3)),
            DaysRange.new(Days.MON, Days.SAT).unwrap(),
        ).unwrap(): (Job.DYNAMO_INTEGRATES,),
    }
)
