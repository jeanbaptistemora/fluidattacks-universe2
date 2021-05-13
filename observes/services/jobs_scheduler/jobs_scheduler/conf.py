# Standard libraries
from typing import (
    Dict,
    List,
)

# Local libraries
from jobs_scheduler.cron import (
    AnyTime,
    PartialCron,
    work_days,
)

SCHEDULE: Dict[PartialCron, List[str]] = {
    PartialCron.new(AnyTime(), AnyTime(), work_days): [
        "observes.job.batch-stability report-failures observes",
    ],
    PartialCron.new(0, AnyTime(), work_days): [
        "observes.scheduled.on-aws.code-etl-mirror",
        "observes.job.batch-stability report-cancelled observes",
    ],
    PartialCron.new(3, AnyTime(), 1): [
        "observes.scheduled.on-aws.bugsnag-etl",
        "observes.scheduled.on-aws.checkly-etl",
        "observes.scheduled.on-aws.delighted-etl",
    ],
    PartialCron.new(6, AnyTime(), work_days): [
        "observes.scheduled.on-aws.code-etl-upload",
    ],
    PartialCron.new(19, AnyTime(), work_days): [
        "observes.scheduled.on-aws.dif-gitlab-etl",
    ],
    PartialCron.new((11, 18), AnyTime(), work_days): [
        "observes.scheduled.on-aws.formstack-etl",
    ],
    PartialCron.new(range(6, 19, 4), AnyTime(), work_days): [
        "observes.scheduled.on-aws.code-etl-amend",
    ],
    PartialCron.new(range(0, 16, 5), AnyTime(), work_days): [
        "observes.scheduled.on-aws.dynamodb-forces-etl",
    ],
    PartialCron.new(range(6, 19, 2), AnyTime(), work_days): [
        "observes.scheduled.on-aws.dynamodb-integrates-etl",
    ],
}
