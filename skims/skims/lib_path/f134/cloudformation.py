from aws.model import (
    AWSS3Bucket,
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
    MethodsEnum,
    Vulnerabilities,
)
from parse_cfn.structure import (
    iter_s3_buckets,
)
from typing import (
    Any,
    Iterator,
    Tuple,
)


def wildcard_in_node(node: Node) -> Tuple[bool, int, int]:
    for rules in node.data:
        for origin in rules.inner.get("AllowedOrigins").data:
            if hasattr(origin, "data") and origin.data == "*":
                return True, origin.start_line, origin.start_column
    return False, 0, 0


def _cfn_wildcard_in_allowed_origins_iterate_vulnerabilities(
    file_ext: str,
    buckets_iterator: Iterator[Node],
) -> Iterator[AWSS3Bucket]:
    for bucket in buckets_iterator:
        if (cors_config := bucket.inner.get("CorsConfiguration")) and (
            cors_rules := cors_config.inner.get("CorsRules")
        ):
            wildcard, line_num, col_num = wildcard_in_node(cors_rules)
            if wildcard:
                yield AWSS3Bucket(
                    column=col_num,
                    data=bucket.data,
                    line=get_line_by_extension(line_num, file_ext),
                )


def cfn_wildcard_in_allowed_origins(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_path.f134.cfn_wildcard_in_allowed_origins",
        iterator=get_cloud_iterator(
            _cfn_wildcard_in_allowed_origins_iterate_vulnerabilities(
                file_ext=file_ext,
                buckets_iterator=iter_s3_buckets(template=template),
            )
        ),
        path=path,
        method=MethodsEnum.CFN_WILDCARD_IN_ALLOWED_ORIGINS,
    )
