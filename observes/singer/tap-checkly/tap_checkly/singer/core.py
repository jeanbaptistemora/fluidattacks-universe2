from enum import (
    Enum,
    unique,
)


@unique
class SingerStreams(Enum):
    alert_channels = "alert_channels"
    check_results = "check_results"
    rolled_check_results = "rolled_check_results"
    rolled_check_results_times = "rolled_check_results_times"
