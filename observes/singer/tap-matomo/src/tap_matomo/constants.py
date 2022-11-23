from typing import (
    Any,
    List,
    Tuple,
)

JSON = Any
_TYPE_STRING: JSON = {"type": "string"}
_TYPE_DATE: JSON = {"type": "string", "format": "date-time"}

WEBSITE_IDS = {
    "1": "Airs",
    "2": "Docs",
    "3": "ASM",
}

REFERRER_TYPES = {
    1: "Direct Entry",
    2: "Search Engines",
    3: "Websites",
    6: "Campaigns",
    7: "Social Networks",
}

# Must set all types to string because the Matomo api
# usually has inconsistent typing
PAGE_PERFORMANCE: JSON = {
    "type": "SCHEMA",
    "stream": "page_performance",
    "key_properties": ["uuid"],
    "schema": {
        "properties": {
            "uuid": _TYPE_STRING,
            "date": _TYPE_DATE,
            "website": _TYPE_STRING,
            "label": _TYPE_STRING,
            "nb_visits": _TYPE_STRING,
            "nb_hits": _TYPE_STRING,
            "sum_time_spent": _TYPE_STRING,
            "entry_nb_visits": _TYPE_STRING,
            "entry_nb_actions": _TYPE_STRING,
            "entry_bounce_count": _TYPE_STRING,
            "exit_nb_visits": _TYPE_STRING,
            "avg_time_network": _TYPE_STRING,
            "avg_time_server": _TYPE_STRING,
            "avg_time_transfer": _TYPE_STRING,
            "avg_time_dom_processing": _TYPE_STRING,
            "avg_time_dom_completion": _TYPE_STRING,
            "avg_time_on_load": _TYPE_STRING,
            "bounce_rate": _TYPE_STRING,
            "exit_rate": _TYPE_STRING,
        }
    },
}

REFERRERS: JSON = {
    "type": "SCHEMA",
    "stream": "referrers",
    "key_properties": ["uuid"],
    "schema": {
        "properties": {
            "uuid": _TYPE_STRING,
            "date": _TYPE_DATE,
            "website": _TYPE_STRING,
            "label": _TYPE_STRING,
            "referer_type": _TYPE_STRING,
            "nb_visits": _TYPE_STRING,
            "nb_actions": _TYPE_STRING,
            "max_actions": _TYPE_STRING,
            "sum_visit_length": _TYPE_STRING,
            "bounce_count": _TYPE_STRING,
        }
    },
}

VISITORS: JSON = {
    "type": "SCHEMA",
    "stream": "visitors",
    "key_properties": ["uuid"],
    "schema": {
        "properties": {
            "uuid": _TYPE_STRING,
            "date": _TYPE_DATE,
            "website": _TYPE_STRING,
            "nb_uniq_visitors": _TYPE_STRING,
            "nb_visits": _TYPE_STRING,
            "nb_actions": _TYPE_STRING,
            "bounce_count": _TYPE_STRING,
            "sum_visit_length": _TYPE_STRING,
            "max_actions": _TYPE_STRING,
            "bounce_rate": _TYPE_STRING,
            "nb_actions_per_visit": _TYPE_STRING,
            "avg_time_on_site": _TYPE_STRING,
        }
    },
}

TABLE_PATTERN_1: JSON = {
    "type": "SCHEMA",
    "stream": "pattern_1",
    "key_properties": ["uuid"],
    "schema": {
        "properties": {
            "uuid": _TYPE_STRING,
            "date": _TYPE_DATE,
            "website": _TYPE_STRING,
            "label": _TYPE_STRING,
            "nb_visits": _TYPE_STRING,
            "nb_hits": _TYPE_STRING,
        }
    },
}

TABLE_PATTERN_2: JSON = {
    "type": "SCHEMA",
    "stream": "pattern_2",
    "key_properties": ["uuid"],
    "schema": {
        "properties": {
            "uuid": _TYPE_STRING,
            "date": _TYPE_DATE,
            "website": _TYPE_STRING,
            "label": _TYPE_STRING,
            "nb_visits": _TYPE_STRING,
            "nb_actions": _TYPE_STRING,
            "max_actions": _TYPE_STRING,
            "sum_visit_length": _TYPE_STRING,
            "bounce_count": _TYPE_STRING,
        }
    },
}

TABLE_PATTERN_3: JSON = {
    "type": "SCHEMA",
    "stream": "pattern_3",
    "key_properties": ["uuid"],
    "schema": {
        "properties": {
            "uuid": _TYPE_STRING,
            "date": _TYPE_DATE,
            "website": _TYPE_STRING,
            "label": _TYPE_STRING,
            "nb_visits": _TYPE_STRING,
        }
    },
}

TABLE_LIST: List[Tuple] = [
    (PAGE_PERFORMANCE, "page_performance", "Actions.getPageUrls"),
    (REFERRERS, "referrers", "Referrers.getAll"),
    (VISITORS, "visitors", "VisitsSummary.get"),
    (TABLE_PATTERN_1, "downloads", "Actions.getDownloads"),
    (TABLE_PATTERN_1, "outlinks", "Actions.getOutlinks"),
    (TABLE_PATTERN_2, "devices", "DevicesDetection.getModel"),
    (TABLE_PATTERN_2, "os", "DevicesDetection.getOsVersions"),
    (TABLE_PATTERN_2, "browsers", "DevicesDetection.getBrowsers"),
    (TABLE_PATTERN_2, "resolutions", "Resolution.getResolution"),
    (TABLE_PATTERN_2, "countries", "UserCountry.getCountry"),
    (TABLE_PATTERN_2, "languages", "UserLanguage.getLanguage"),
    (
        TABLE_PATTERN_2,
        "visits_per_local_time",
        "VisitTime.getVisitInformationPerLocalTime",
    ),
    (
        TABLE_PATTERN_2,
        "visits_per_server_time",
        "VisitTime.getVisitInformationPerServerTime",
    ),
    (TABLE_PATTERN_2, "visits_per_week_day", "VisitTime.getByDayOfWeek"),
    (
        TABLE_PATTERN_3,
        "visits_per_visit_duration",
        "VisitorInterest.getNumberOfVisitsPerVisitDuration",
    ),
    (
        TABLE_PATTERN_3,
        "visits_per_pages_visited",
        "VisitorInterest.getNumberOfVisitsPerPage",
    ),
    (
        TABLE_PATTERN_3,
        "visits_per_return_time",
        "VisitorInterest.getNumberOfVisitsByDaysSinceLast",
    ),
    (
        TABLE_PATTERN_3,
        "visitors_per_visit_count",
        "VisitorInterest.getNumberOfVisitsByVisitCount",
    ),
]
