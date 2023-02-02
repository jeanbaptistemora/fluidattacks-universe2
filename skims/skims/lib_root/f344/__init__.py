from lib_root.f344.javascript import (
    js_local_storage_sens_data_async,
    js_local_storage_with_sensitive_data as js_local_storage_sensitive_data,
)
from lib_root.f344.typescript import (
    ts_local_storage_sens_data_async,
    ts_local_storage_with_sensitive_data as ts_local_storage_sensitive_data,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F344
QUERIES: graph_model.Queries = (
    (FINDING, js_local_storage_sensitive_data),
    (FINDING, ts_local_storage_sensitive_data),
    (FINDING, js_local_storage_sens_data_async),
    (FINDING, ts_local_storage_sens_data_async),
)
