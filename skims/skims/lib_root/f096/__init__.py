from lib_root.f096.c_sharp import (
    check_xml_serializer as c_sharp_check_xml_serializer,
    insecure_deserialization as c_sharp_insecure_deserialization,
    js_deserialization as c_sharp_js_deserialization,
    type_name_handling as c_sharp_type_name_handling,
)
from lib_root.f096.python import (
    python_deserialization_injection,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F096
QUERIES: graph_model.Queries = (
    (FINDING, c_sharp_insecure_deserialization),
    (FINDING, c_sharp_check_xml_serializer),
    (FINDING, c_sharp_js_deserialization),
    (FINDING, c_sharp_type_name_handling),
    (FINDING, python_deserialization_injection),
)
