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
    PartialCron.new(0, AnyTime(), work_days): [
        "observes.scheduled.on-aws.code-etl-mirror",
    ],
    PartialCron.new(6, AnyTime(), work_days): [
        "observes.scheduled.on-aws.code-etl-upload",
    ],
    PartialCron.new(19, AnyTime(), work_days): [
        "observes.scheduled.on-aws.dif-gitlab-etl",
    ],
}
