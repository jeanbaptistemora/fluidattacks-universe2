from lib_root.f060.c_sharp import (
    insecure_certificate_validation as csharp_insecure_certificate_validation,
)
from lib_root.f060.conf_files import (
    allowed_hosts as json_allowed_hosts,
    disable_host_check as json_disable_host_check,
)
from lib_root.f060.javascript import (
    unsafe_origin as js_unsafe_origin,
)
from lib_root.f060.typescript import (
    unsafe_origin as ts_unsafe_origin,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F060
QUERIES: graph_model.Queries = (
    (FINDING, csharp_insecure_certificate_validation),
    (FINDING, ts_unsafe_origin),
    (FINDING, json_allowed_hosts),
    (FINDING, json_disable_host_check),
    (FINDING, js_unsafe_origin),
)
