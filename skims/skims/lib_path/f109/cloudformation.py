from aws.model import (
    AWSRdsCluster,
)
from lib_path.common import (
    get_cloud_iterator,
    get_line_by_extension,
    get_vulnerabilities_from_iterator_blocking,
)
from metaloaders.model import (
    Node,
)
from model.core_model import (
    DeveloperEnum,
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


def _cfn_rds_is_not_inside_a_db_subnet_group_iterate_vulnerabilities(
    file_ext: str,
    rds_iterator: Iterator[Union[AWSRdsCluster, Node]],
) -> Iterator[Union[AWSRdsCluster, Node]]:
    for rds_res in rds_iterator:
        if "DBSubnetGroupName" not in rds_res.raw:
            yield AWSRdsCluster(
                column=rds_res.start_column,
                data=rds_res.data,
                line=get_line_by_extension(rds_res.start_line, file_ext),
            )


def cfn_rds_is_not_inside_a_db_subnet_group(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F109.value.cwe},
        description_key=(
            "src.lib_path.f109.rds_is_not_inside_a_db_subnet_group"
        ),
        finding=FindingEnum.F109,
        iterator=get_cloud_iterator(
            _cfn_rds_is_not_inside_a_db_subnet_group_iterate_vulnerabilities(
                file_ext=file_ext,
                rds_iterator=iter_rds_clusters_and_instances(
                    template=template
                ),
            )
        ),
        path=path,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
    )
