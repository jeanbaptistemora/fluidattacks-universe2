from aws.model import (
    AWSServerlessApi,
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
    iter_severless_api,
)
from typing import (
    Any,
)
from utils.function import (
    get_node_by_keys,
)


def _method_sethings_has_http_methods_enabled(
    buckets_iterator: Iterator[Node],
) -> Iterator[AWSServerlessApi]:
    for bucket in buckets_iterator:
        methods = get_node_by_keys(bucket, ["MethodSettings"])
        if methods:
            for meth in methods.data:
                http_method = get_node_by_keys(meth, ["HttpMethod"])
                if http_method and http_method.data == "*":
                    yield AWSServerlessApi(
                        column=http_method.start_column,
                        data=http_method.data,
                        line=http_method.start_line,
                    )


def severless_bucket_has_https_methos_enabled(
    content: str,
    path: str,
    template: Any,
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=(
            "src.lib_path.f044.severless_bucket_has_https_methos_enabled"
        ),
        iterator=get_cloud_iterator(
            _method_sethings_has_http_methods_enabled(
                buckets_iterator=iter_severless_api(template=template),
            )
        ),
        path=path,
        method=MethodsEnum.CNF_HTTP_METHODS_ENABLED,
    )
