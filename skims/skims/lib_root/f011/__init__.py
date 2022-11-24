from lib_root.f011.c_sharp import (
    schema_by_url as c_sharp_schema_by_url,
    xsl_transform_object as c_sharp_xsl_transform_object,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F011
QUERIES: graph_model.Queries = (
    (FINDING, c_sharp_xsl_transform_object),
    (FINDING, c_sharp_schema_by_url),
)
