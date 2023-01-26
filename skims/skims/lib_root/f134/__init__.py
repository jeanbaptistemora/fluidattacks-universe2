from lib_root.f134.c_sharp import (
    insecure_cors as csharp_insecure_cors,
    insecure_cors_origin as csharp_insecure_cors_origin,
)
from lib_root.f134.cloudformation import (
    wildcard_in_allowed_origins as cfn_wildcard_in_allowed_origins,
)
from lib_root.f134.conf_files import (
    serverles_cors_true,
)
from lib_root.f134.java import (
    insecure_cors_origin as java_insecure_cors_origin,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F134
QUERIES: graph_model.Queries = (
    (FINDING, cfn_wildcard_in_allowed_origins),
    (FINDING, csharp_insecure_cors),
    (FINDING, csharp_insecure_cors_origin),
    (FINDING, java_insecure_cors_origin),
    (FINDING, serverles_cors_true),
)
