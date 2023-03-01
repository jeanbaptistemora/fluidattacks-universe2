from lib_root.f335.cloudformation import (
    cfn_s3_bucket_versioning_disabled,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F335
QUERIES: graph_model.Queries = ((FINDING, cfn_s3_bucket_versioning_disabled),)
