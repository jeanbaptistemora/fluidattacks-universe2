from lib_path.common import (
    get_cloud_iterator,
    get_vulnerabilities_from_iterator_blocking,
)
from metaloaders.model import (
    Node,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from parse_hcl2.structure.aws import (
    iterate_iam_policy_documents,
)
from typing import (
    Any,
    Iterator,
    Union,
)


def _service_is_present_action(
    actions: Union[str, list], service: str
) -> bool:
    actions = actions if isinstance(actions, list) else [actions]
    for act in actions:
        if act == "*" or act.split(":")[0] == service:
            return True
    return False


def _tfm_iam_has_privileges_over_iam_iter_vulns(
    resource_iterator: Iterator[Any],
) -> Iterator[Union[Any, Node]]:
    for stmt in resource_iterator:
        effect = stmt.data.get("Effect", "")
        actions = stmt.data.get("Action", [])
        if effect == "Allow" and _service_is_present_action(actions, "iam"):
            yield stmt


def tfm_iam_has_privileges_over_iam(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f325.tfm_iam_has_privileges_over_iam",
        iterator=get_cloud_iterator(
            _tfm_iam_has_privileges_over_iam_iter_vulns(
                resource_iterator=iterate_iam_policy_documents(model=model)
            )
        ),
        path=path,
        method=MethodsEnum.EC2_IAM_PRIVILEGES_OVER_IAM,
    )
