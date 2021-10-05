from model import (
    core_model,
    graph_model,
)
from sast_transformations.danger_nodes.utils import (
    append_label_input,
)
from utils.string import (
    complete_attrs_on_set,
)

FINDINGS = {
    core_model.FindingEnum.F001,
    core_model.FindingEnum.F004,
    core_model.FindingEnum.F008,
    core_model.FindingEnum.F021,
    core_model.FindingEnum.F063,
    core_model.FindingEnum.F107,
}


def mark_metadata(
    graph: graph_model.Graph,
    metadata: graph_model.GraphShardMetadata,
) -> None:
    danger_superclass = complete_attrs_on_set(
        {
            "System.Web.Http.ApiController",
            "Microsoft.AspNetCore.Mvc.Controller",
        }
    )
    http_actions = {"Post", "Delete", "Get", "Put"}
    danger_attributes = {
        "HttpGet",
        "HttpPut",
        "HttpPost",
        "HttpDelete",
    }
    danger_classes = tuple(
        _class
        for _class in metadata.c_sharp.classes.values()
        if _class.inherit in danger_superclass
    )
    for _class in danger_classes:
        danger_methods = tuple(
            _method
            for _method in _class.methods.values()
            if any(_method.name.startswith(action) for action in http_actions)
            or (
                set(getattr(_method, "attributes", [])).intersection(
                    danger_attributes
                )
            )
        )
        parameters = tuple(
            _parameter
            for _method in danger_methods
            for _parameter in _method.parameters.values()
        )
        for _parameter in parameters:
            for finding in FINDINGS:
                append_label_input(graph, _parameter.n_id, finding)
