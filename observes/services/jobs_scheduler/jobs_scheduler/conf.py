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
        os.environ["batchStability"] + " report-failures observes",
    ],
    PartialCron.new(0, AnyTime(), work_days): [
        os.environ["codeEtlMirror"],
        os.environ["batchStability"] + " report-cancelled observes",
    ],
    PartialCron.new(3, AnyTime(), 1): [
        os.environ["announceKitEtl"],
        os.environ["bugsnagEtl"],
        os.environ["checklyEtl"],
        os.environ["delightedEtl"],
    ],
    PartialCron.new(6, AnyTime(), work_days): [
        os.environ["codeEtlUpload"],
    ],
    PartialCron.new(range(0, 24, 2), AnyTime(), AnyTime()): [
        os.environ["gitlabEtlProduct"],
    ],
    PartialCron.new(range(1, 24, 2), AnyTime(), AnyTime()): [
        os.environ["gitlabEtlChallenges"],
        os.environ["gitlabEtlDefault"],
        os.environ["gitlabEtlServices"],
    ],
    PartialCron.new((11, 18), AnyTime(), work_days): [
        os.environ["formstackEtl"],
    ],
    PartialCron.new(range(0, 16, 5), AnyTime(), work_days): [
        os.environ["dynamoDbForcesEtl"],
    ],
    PartialCron.new(range(5, 19, 3), AnyTime(), work_days): [
        os.environ["dynamoDbIntegratesEtl"],
    ],
    PartialCron.new(range(5, 19, 5), AnyTime(), work_days): [
        os.environ["dynamoTableEtlBig"] + "integrates_vms",
    ],
    PartialCron.new(range(3, 19, 5), AnyTime(), work_days): [
        os.environ["dynamoTableEtlBig"] + "FI_vulnerabilities",
    ],
}
