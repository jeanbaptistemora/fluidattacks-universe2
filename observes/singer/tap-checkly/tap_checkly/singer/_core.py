from enum import (
    Enum,
    unique,
)


@unique
class SingerStreams(Enum):
    alert_channels = "alert_channels"
    checks = "checks"
    check_status = "check_status"
    check_reports = "check_reports"
    check_groups = "check_groups"
    check_groups_alerts = "check_groups_alerts"
    check_groups_locations = "check_groups_locations"
    check_locations = "check_locations"
    check_results = "check_results"
    check_results_api = "check_results_api"
    check_results_browser = "check_results_browser"
    check_results_browser_pages = "check_results_browser_pages"
