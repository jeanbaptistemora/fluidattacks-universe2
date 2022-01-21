from aws.model import (
    AWSRdsCluster,
)
from lib_path.common import (
    get_cloud_iterator,
    get_vulnerabilities_from_iterator_blocking,
    TRUE_OPTIONS,
)
from metaloaders.model import (
    Node,
)
from model.core_model import (
    FindingEnum,
    Vulnerabilities,
)
from parse_cfn.structure import (
    iter_rds_clusters_and_instances,
)
from typing import (
    Any,
    Iterator,
    Union,
)
from utils.function import (
    get_node_by_keys,
)


def _cfn_rds_is_publicly_accessible_iterate_vulnerabilities(
    rds_iterator: Iterator[Union[AWSRdsCluster, Node]],
) -> Iterator[Union[AWSRdsCluster, Node]]:
    for rds_res in rds_iterator:
        publicy_acc = get_node_by_keys(rds_res, ["PubliclyAccessible"])
        if isinstance(publicy_acc, Node) and publicy_acc.raw in TRUE_OPTIONS:
            yield publicy_acc


def cfn_rds_is_publicly_accessible(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F073.value.cwe},
        description_key="src.lib_path.f073.rds_is_publicly_accessible",
        finding=FindingEnum.F073,
        iterator=get_cloud_iterator(
            _cfn_rds_is_publicly_accessible_iterate_vulnerabilities(
                rds_iterator=iter_rds_clusters_and_instances(
                    template=template
                ),
            )
        ),
        path=path,
    )
