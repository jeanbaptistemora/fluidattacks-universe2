from aws.model import (
    AWSRdsCluster,
)
from lib_path.common import (
    get_cloud_iterator,
    get_line_by_extension,
    get_vulnerabilities_from_iterator_blocking,
    TRUE_OPTIONS,
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


def _cfn_rds_has_unencrypted_storage_iterate_vulnerabilities(
    file_ext: str,
    rds_iterator: Iterator[Node],
) -> Iterator[Union[AWSRdsCluster, Node]]:
    for red_res in rds_iterator:
        storage_encrypted = red_res.raw.get("StorageEncrypted", False)
        if storage_encrypted not in TRUE_OPTIONS:
            st_enc_node = get_node_by_keys(red_res, ["StorageEncrypted"])
            if isinstance(st_enc_node, Node):
                yield st_enc_node
            else:
                yield AWSRdsCluster(
                    column=red_res.start_column,
                    data=red_res.data,
                    line=get_line_by_extension(red_res.start_line, file_ext),
                )


def cfn_rds_has_unencrypted_storage(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f246.rds_has_unencrypted_storage",
        iterator=get_cloud_iterator(
            _cfn_rds_has_unencrypted_storage_iterate_vulnerabilities(
                file_ext=file_ext,
                rds_iterator=iter_rds_clusters_and_instances(
                    template=template
                ),
            )
        ),
        path=path,
        method=MethodsEnum.CFN_RDS_UNENCRYPTED_STORAGE,
    )
