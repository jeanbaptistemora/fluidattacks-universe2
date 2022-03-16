# FP: local testing
from back.src.settings.logger import (
    LOGGING,
)
import logging
import matplotlib
from reports.typing import (
    CertFindingInfo,
)
from typing import (
    List,
    Optional,
    Tuple,
    TypedDict,
    Union,
)

logging.config.dictConfig(LOGGING)  # NOSONAR
matplotlib.use("Agg")


# Constants
LOGGER = logging.getLogger(__name__)
RemediationTable = TypedDict(
    "RemediationTable",
    {
        "table": List[List[Union[float, int, str]]],
    },
)
Context = TypedDict(
    "Context",
    {
        "business": str,
        "business_number": str,
        "solution": str,
        "start_date": str,
        "report_date": str,
        "team": str,
        "team_mail": str,
        "customer": str,
        "version": str,
        "revdate": str,
        "simpledate": str,
        "remediation_table": RemediationTable,
        "findings": Tuple[CertFindingInfo, ...],
        "accessVector": Optional[str],
        "cert_title": str,
        "crit_h": str,
        "crit_m": str,
        "crit_l": str,
        "field": str,
        "user": str,
        "date": str,
        "link": str,
    },
)
