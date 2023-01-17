from aws.model import (
    AWSRdsCluster,
)
from lib_path.common import (
    FALSE_OPTIONS,
    get_cloud_iterator,
    get_line_by_extension,
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
    Iterator,
    Union,
)
from utils.function import (
    get_node_by_keys,
)


def _cfn_rds_has_not_automated_backups_iterate_vulnerabilities(
    rds_iterator: Iterator[Union[AWSRdsCluster, Node]],
) -> Iterator[Union[AWSRdsCluster, Node]]:
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


def _cfn_rds_has_not_termination_protection_iterate_vulnerabilities(
    file_ext: str,
    rds_iterator: Iterator[Node],
) -> Iterator[Union[AWSRdsCluster, Node]]:
    for rds_res in rds_iterator:
        del_protection_node = get_node_by_keys(rds_res, ["DeletionProtection"])
        if isinstance(del_protection_node, Node):
            if del_protection_node.data in FALSE_OPTIONS:
                yield del_protection_node
        else:
            yield AWSRdsCluster(
                column=rds_res.start_column,
                data=rds_res.data,
                line=get_line_by_extension(rds_res.start_line, file_ext),
            )


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


def cfn_rds_has_not_termination_protection(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f256.rds_has_not_termination_protection",
        iterator=get_cloud_iterator(
            _cfn_rds_has_not_termination_protection_iterate_vulnerabilities(
                file_ext=file_ext,
                rds_iterator=iter_rds_clusters_and_instances(
                    template=template
                ),
            )
        ),
        path=path,
        method=MethodsEnum.CFN_RDS_NOT_TERMINATION_PROTEC,
    )
