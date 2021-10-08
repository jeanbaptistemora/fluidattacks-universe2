from metaloaders.model import (
    Node,
)
from typing import (
    Any,
    Iterator,
    Union,
)


def _serves_content_over_http_iterate_vulnerabilities(
    distributions_iterator: Iterator[Union[Any, Node]]
) -> Iterator[Union[Any, Node]]:
    for dist in distributions_iterator:
        dist_config = dist.inner["DistributionConfig"]
        if isinstance(dist_config, Node):
            if "DefaultCacheBehavior" in dist_config.inner:
                def_cache_beh = dist_config.inner["DefaultCacheBehavior"]
                if (
                    isinstance(def_cache_beh, Node)
                    and "ViewerProtocolPolicy" in def_cache_beh.inner
                    and def_cache_beh.raw["ViewerProtocolPolicy"]
                    == "allow-all"
                ):
                    yield def_cache_beh.inner["ViewerProtocolPolicy"]
            if "CacheBehaviors" in dist_config.inner and isinstance(
                dist_config.inner["CacheBehaviors"], Node
            ):
                cache_behaviors = dist_config.inner["CacheBehaviors"]
                for cache_b in cache_behaviors.data:
                    if (
                        "ViewerProtocolPolicy" in cache_b.inner
                        and cache_b.raw["ViewerProtocolPolicy"] == "allow-all"
                    ):
                        yield cache_b.inner["ViewerProtocolPolicy"]
