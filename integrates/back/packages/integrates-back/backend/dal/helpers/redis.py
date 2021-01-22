# Standard library
import asyncio
from typing import (
    Any,
)

# Third party libraries
from aioextensions import (
    in_thread,
)
from redis.exceptions import (
    RedisError,
)
from rediscluster import (
    RedisCluster,
)
from rediscluster.exceptions import (
    RedisClusterConfigError,
    RedisClusterException,
    RedisClusterError,
    ClusterDownException,
)

# Local libraries
from __init__ import (
    FI_REDIS_SERVER,
)

# A cluster is different than a server
# the cluster is a distributed system whereas the server is standalone.
#
# Commands available in one may not be available in the other
#
# https://redis-py.readthedocs.io/en/stable
# https://redis-py-cluster.readthedocs.io/en/stable

# Constants
REDIS_EXCEPTIONS = (
    AttributeError,
    ClusterDownException,
    OSError,
    RedisClusterConfigError,
    RedisClusterException,
    RedisClusterError,
    RedisError,
)
REDIS_TIMEOUT: int = 30


async def _redis_cmd_base(cmd: str, *args: Any, **kwargs: Any) -> Any:
    cmd_func = getattr(REDIS, cmd)
    data = await asyncio.wait_for(
        in_thread(cmd_func, *args, **kwargs),
        timeout=REDIS_TIMEOUT,
    )

    return data


async def redis_cmd(cmd: str, *args: Any, **kwargs: Any) -> Any:
    try:
        return await _redis_cmd_base(cmd, *args, **kwargs)
    except ClusterDownException:
        # Regenerate redis cluster object so it points to the new internal IP
        global REDIS  # pylint: disable=global-statement
        REDIS = instantiate_redis_cluster()

        # Retry the command
        return await _redis_cmd_base(cmd, *args, **kwargs)


def instantiate_redis_cluster() -> RedisCluster:
    return RedisCluster(
        cluster_down_retry_attempts=1,
        decode_responses=True,
        host=FI_REDIS_SERVER,
        max_connections=1024,
        port=6379,
        skip_full_coverage_check=True,
    )


# Import hooks
REDIS = instantiate_redis_cluster()
