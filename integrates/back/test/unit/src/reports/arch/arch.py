from arch_lint.dag import (
    DagMap,
)
from typing import (
    cast,
    Dict,
    Tuple,
    Union,
)

_dag: Dict[str, Tuple[Union[Tuple[str, ...], str], ...]] = {
    "reports": (
        "domain",
        "report_types",
        "standard_report",
        "certificate",
        "pdf",
        "secure_pdf",
        "it_report",
        "typing",
    ),
    "reports.report_types": (
        "data",
        "technical",
        "certificate",
        "unfulfilled_standards",
    ),
}


def project_dag() -> DagMap:
    return cast(DagMap, DagMap.new(_dag))
