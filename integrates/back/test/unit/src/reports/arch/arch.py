from arch_lint.dag import (
    DagMap,
)
from typing import (
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
    result = DagMap.new(_dag)
    if isinstance(result, Exception):
        raise result
    return result
