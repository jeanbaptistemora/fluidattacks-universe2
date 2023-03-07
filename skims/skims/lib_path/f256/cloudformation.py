from aws.model import (
    AWSRdsCluster,
)
from collections.abc import (
    Iterator,
)
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
from parse_cfn.structure import (
    iter_rds_clusters_and_instances,
)
from typing import (
    Any,
)
from utils.function import (
    get_node_by_keys,
)


def _cfn_rds_has_not_automated_backups_iterate_vulnerabilities(
    rds_iterator: Iterator[AWSRdsCluster | Node],
) -> Iterator[AWSRdsCluster | Node]:
    for rds_res in rds_iterator:
        ret_period = get_node_by_keys(
            rds_res, ["BackupRetentionPeriod"]  # type: ignore
        )
        if (
            hasattr(ret_period, "raw")
            and isinstance(ret_period, Node)
            and ret_period.raw in (0, "0")
        ):
            yield ret_period


def cfn_rds_has_not_automated_backups(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f256.rds_has_not_automated_backups",
        iterator=get_cloud_iterator(
            _cfn_rds_has_not_automated_backups_iterate_vulnerabilities(
                rds_iterator=iter_rds_clusters_and_instances(
                    template=template
                ),
            )
        ),
        path=path,
        method=MethodsEnum.CFN_RDS_NOT_AUTO_BACKUPS,
    )
