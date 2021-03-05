# Standard library
import asyncio
import logging
from typing import (
    Any,
    Awaitable,
    Callable,
    Optional,
    Set,
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
from back import (
    settings,
)
from backend.model import (
    redis_model,
)
from newutils.serialization import (
    dump,
    load,
)

# A cluster is different than a server
# the cluster is a distributed system whereas the server is standalone.
#
# Commands available in one may not be available in the other
#
# https://redis-py.readthedocs.io/en/stable
# https://redis-py-cluster.readthedocs.io/en/stable

# Constants
LOGGER = logging.getLogger(__name__)
REDIS: RedisCluster = None
REDIS_EXCEPTIONS = (
    AttributeError,
    ClusterDownException,
    OSError,
    RedisClusterConfigError,
    RedisClusterException,
    RedisClusterError,
    RedisError,
    UnboundLocalError,
)
REDIS_TIMEOUT: int = 30


async def _redis_cmd_base(cmd: str, *args: Any, **kwargs: Any) -> Any:
    if REDIS is None:
        raise ClusterDownException()
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


async def redis_exists_entity_attr(
    *,
    entity: str,
    attr: str,
    **args: str,
) -> bool:
    # https://redis.io/commands/exists

    key: str = redis_model.build_key(entity, attr, **args)
    response: int = await redis_cmd('exists', key)

    return response == 1


async def redis_ttl_entity_attr(
    *,
    entity: str,
    attr: str,
    **args: str,
) -> int:
    # https://redis.io/commands/ttl

    key: str = redis_model.build_key(entity, attr, **args)
    response: int = await redis_cmd('ttl', key)

    return response


async def redis_set_entity_attr(
    *,
    entity: str,
    attr: str,
    value: Any,
    ttl: int = settings.CACHE_TTL,
    **args: str,
) -> bool:
    # https://redis.io/commands/setex

    key: str = redis_model.build_key(entity, attr, **args)
    value_encoded: bytes = dump(value)
    success: bool = await redis_cmd('setex', key, ttl, value_encoded)

    return success


async def redis_get_entity_attr(
    *,
    entity: str,
    attr: str,
    **args: str,
) -> Any:
    # https://redis.io/commands/get

    key: str = redis_model.build_key(entity, attr, **args)
    response: Optional[bytes] = await redis_cmd('get', key)

    if response is None:
        # Not found
        raise redis_model.KeyNotFound()

    # Deserialize and return
    result: Any = load(response)

    return result


async def redis_get_or_set_entity_attr(
    generator: Callable[[], Awaitable[Any]],
    *,
    entity: str,
    attr: str,
    ttl: int = settings.CACHE_TTL,
    **args: str,
) -> Any:
    try:
        try:
            response: Any = await redis_get_entity_attr(
                entity=entity,
                attr=attr,
                **args,
            )
        except redis_model.KeyNotFound:
            response = await generator()

            await redis_set_entity_attr(
                entity=entity,
                attr=attr,
                value=response,
                ttl=ttl,
                **args,
            )

    except REDIS_EXCEPTIONS as ex:
        LOGGER.exception(ex, extra=dict(extra=locals()))
        response = await generator()

    return response


async def redis_del_entity_attr(
    entity: str,
    attr: str,
    **args: str,
) -> bool:
    # https://redis.io/commands/del

    key: str = redis_model.build_key(entity, attr, **args)
    response: bool = await redis_cmd('delete', key) == 1

    return response


def redis_del_entity_attr_soon(
    entity: str,
    attr: str,
    **args: str,
) -> None:
    # Candidate to be pushed into the daemon queue
    asyncio.create_task(redis_del_entity_attr(entity, attr, **args))


async def redis_del_entity(
    entity: str,
    **args: str,
) -> bool:
    # https://redis.io/commands/del

    keys: Set[str] = redis_model.build_keys_for_entity(entity, **args)
    response: bool = (
        await redis_cmd('delete', *keys) == len(keys)
        if keys
        else True
    )

    return response


def redis_del_entity_soon(
    entity: str,
    **args: str,
) -> None:
    # Candidate to be pushed into the daemon queue
    asyncio.create_task(redis_del_entity(entity, **args))


async def redis_del_by_deps(dependency: str, **args: str) -> bool:
    keys: Set[str] = redis_model.build_keys_by_dependencies(dependency, **args)

    response: bool = (
        await redis_cmd('delete', *keys) == len(keys)
        if keys
        else True
    )

    return response


def redis_del_by_deps_soon(dependency: str, **args: str) -> None:
    # Candidate to be pushed into the daemon queue
    asyncio.create_task(redis_del_by_deps(dependency, **args))


def instantiate_redis_cluster() -> RedisCluster:
    return RedisCluster(
        cluster_down_retry_attempts=1,
        decode_responses=True,
        host=FI_REDIS_SERVER,
        max_connections=1024,
        port=6379,
        skip_full_coverage_check=True,
    )
