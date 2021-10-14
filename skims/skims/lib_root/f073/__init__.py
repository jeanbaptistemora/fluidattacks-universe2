from lib_root.f073.c_sharp import (
    switch_without_default as c_sharp_switch_without_default,
)
from lib_root.f073.go import (
    switch_without_default as go_switch_without_default,
)
from lib_root.f073.java import (
    switch_without_default as java_switch_without_default,
)
from lib_root.f073.javascript import (
    switch_without_default as javascript_switch_without_default,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F073
QUERIES: graph_model.Queries = (
    (FINDING, c_sharp_switch_without_default),
    (FINDING, go_switch_without_default),
    (FINDING, java_switch_without_default),
    (FINDING, javascript_switch_without_default),
)
