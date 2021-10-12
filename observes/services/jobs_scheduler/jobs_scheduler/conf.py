from jobs_scheduler.cron import (
    AnyTime,
    PartialCron,
    work_days,
)
import os
from typing import (
    Dict,
    List,
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
        os.environ["bugsnagEtl"],
        os.environ["checklyEtl"],
        "observes.scheduled.on-aws.delighted-etl",
    ],
    PartialCron.new(6, AnyTime(), work_days): [
        "observes.scheduled.on-aws.code-etl-upload",
    ],
    PartialCron.new(range(0, 24, 2), AnyTime(), AnyTime()): [
        "observes.scheduled.on-aws.gitlab-etl.product",
    ],
    PartialCron.new(range(1, 24, 2), AnyTime(), AnyTime()): [
        "observes.scheduled.on-aws.gitlab-etl.challenges",
        "observes.scheduled.on-aws.gitlab-etl.default",
        "observes.scheduled.on-aws.gitlab-etl.services",
    ],
    PartialCron.new((11, 18), AnyTime(), work_days): [
        "observes.scheduled.on-aws.formstack-etl",
    ],
    PartialCron.new(range(7, 21, 4), AnyTime(), work_days): [
        os.environ["codeEtlAmend"],
    ],
    PartialCron.new(range(0, 16, 5), AnyTime(), work_days): [
        "observes.scheduled.on-aws.dynamodb-forces-etl",
    ],
    PartialCron.new(range(6, 19, 3), AnyTime(), work_days): [
        "observes.scheduled.on-aws.dynamodb-integrates-etl",
    ],
}
