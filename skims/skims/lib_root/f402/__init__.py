from lib_root.f402.terraform import (
    tfm_azure_app_service_logging_disabled,
    tfm_azure_sql_server_audit_log_retention,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F402
QUERIES: graph_model.Queries = (
    (FINDING, tfm_azure_app_service_logging_disabled),
    (FINDING, tfm_azure_sql_server_audit_log_retention),
)
