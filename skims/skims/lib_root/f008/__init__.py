from lib_root.f008.c_sharp import (
    insec_addheader_write as c_sharp_insec_addheader_write,
)
from lib_root.f008.java import (
    unsafe_xss_content as java_unsafe_xss_content,
)
from lib_root.f008.javascript import (
    unsafe_xss_content as js_unsafe_xss_content,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F008
QUERIES: graph_model.Queries = (
    (FINDING, c_sharp_insec_addheader_write),
    (FINDING, java_unsafe_xss_content),
    (FINDING, js_unsafe_xss_content),
)
