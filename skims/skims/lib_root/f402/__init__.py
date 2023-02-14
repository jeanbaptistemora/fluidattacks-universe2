from lib_root.f402.terraform import (
    tfm_azure_app_service_logging_disabled,
    tfm_azure_sql_server_audit_log_retention,
    tfm_azure_storage_logging_disabled,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F402
QUERIES: graph_model.Queries = (
    (FINDING, tfm_azure_app_service_logging_disabled),
    (FINDING, tfm_azure_sql_server_audit_log_retention),
    (FINDING, tfm_azure_storage_logging_disabled),
)
