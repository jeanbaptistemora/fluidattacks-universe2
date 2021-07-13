from datetime import (
    datetime,
)
from tap_gitlab.intervals.fragmented import (
    FIntervalFactory,
)
from tap_gitlab.intervals.interval.factory import (
    IntervalFactory,
)
from tap_gitlab.intervals.progress import (
    FProgressFactory,
)
from tap_gitlab.state._objs import (
    JobStatePoint,
)

factory = IntervalFactory.from_default(datetime)
f_factory = FIntervalFactory(factory)
fp_factory = FProgressFactory(f_factory)


def greatter(p_1: JobStatePoint, p_2: JobStatePoint) -> bool:
    return p_1[0] > p_2[0]


factory_2 = IntervalFactory(greatter)
f_factory_2 = FIntervalFactory(factory_2)
fp_factory_2 = FProgressFactory(f_factory_2)
