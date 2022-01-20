from metaloaders.model import (
    Node,
)
from parse_hcl2.tokens import (
    Attribute,
)
from typing import (
    Any,
    Iterator,
    Union,
)


def tfm_rds_has_unencrypted_storage_iterate_vulnerabilities(
    resource_iterator: Iterator[Any],
) -> Iterator[Union[Any, Node]]:
    for resource in resource_iterator:
        protection_attr = False
        for elem in resource.data:
            if isinstance(elem, Attribute) and elem.key == "storage_encrypted":
                protection_attr = True
                if elem.val is False:
                    yield elem
        if not protection_attr:
            yield resource
