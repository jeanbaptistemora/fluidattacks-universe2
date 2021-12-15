from jobs_scheduler.cron_2.core import (
    AnyTime,
    Cron,
)
from jobs_scheduler.cron_2.factory import (
    weekly,
    work_days,
)
import os
from purity.v2.frozen import (
    FrozenDict,
    FrozenList,
)

ANY = AnyTime()
SCHEDULE: FrozenDict[Cron, FrozenList[str]] = FrozenDict(
    {
        work_days(ANY, ANY).unwrap(): (
            os.environ["batchStability"] + " report-failures observes",
        ),
        work_days(ANY, 0).unwrap(): (
            os.environ["codeEtlMirror"],
            os.environ["batchStability"] + " report-cancelled observes",
        ),
        weekly(ANY, 3, 1).unwrap(): (
            os.environ["announceKitEtl"],
            os.environ["bugsnagEtl"],
            os.environ["checklyEtl"],
            os.environ["delightedEtl"],
        ),
        work_days(ANY, 6).unwrap(): (os.environ["codeEtlUpload"],),
        work_days(ANY, range(7, 19, 2)).unwrap(): (
            os.environ["gitlabEtlProduct"],
            os.environ["gitlabEtlChallenges"],
            os.environ["gitlabEtlDefault"],
            os.environ["gitlabEtlServices"],
        ),
        work_days(ANY, (11, 18)).unwrap(): (os.environ["formstackEtl"],),
        work_days(ANY, range(0, 16, 5)).unwrap(): (
            os.environ["dynamoDbForcesEtl"],
        ),
        work_days(ANY, range(5, 19, 3)).unwrap(): (
            os.environ["dynamoDbIntegratesEtl"],
        ),
        work_days(ANY, range(5, 19, 5)).unwrap(): (
            os.environ["dynamoTableEtlBig"] + " integrates_vms",
        ),
    }
)
