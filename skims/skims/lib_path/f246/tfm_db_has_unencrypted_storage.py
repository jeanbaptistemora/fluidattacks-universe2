from lib_path.common import (
    get_cloud_iterator,
    get_vulnerabilities_from_iterator_blocking,
)
from lib_path.f246.utils import (
    tfm_rds_has_unencrypted_storage_iterate_vulnerabilities,
)
from model.core_model import (
    FindingEnum,
    Vulnerabilities,
)
from parse_hcl2.structure.aws import (
    iter_aws_db_instance,
)
from typing import (
    Any,
)


def tfm_db_has_unencrypted_storage(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F246.value.cwe},
        description_key="src.lib_path.f246.rds_has_unencrypted_storage",
        finding=FindingEnum.F246,
        iterator=get_cloud_iterator(
            tfm_rds_has_unencrypted_storage_iterate_vulnerabilities(
                resource_iterator=iter_aws_db_instance(model=model)
            )
        ),
        path=path,
    )
