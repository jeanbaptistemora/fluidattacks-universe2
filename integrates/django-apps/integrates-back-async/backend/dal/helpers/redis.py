
from aredis import (
    StrictRedis as AStrictRedis,
    StrictRedisCluster as AStrictRedisCluster,
)
from redis import StrictRedis
from rediscluster import RedisCluster
from __init__ import FI_ENVIRONMENT, FI_REDIS_SERVER

if FI_ENVIRONMENT == 'development':
    REDIS_CLIENT = StrictRedis(
        host=FI_REDIS_SERVER,
        port=6379,
        db=0,
        decode_responses=True)

    AREDIS_CLIENT = AStrictRedis(
        host=FI_REDIS_SERVER,
        port=6379,
        db=0,
        decode_responses=True
    )
else:
    REDIS_CLIENT = RedisCluster(
        startup_nodes=[{'host': FI_REDIS_SERVER, 'port': '6379'}],
        decode_responses=True,
        skip_full_coverage_check=True)

    AREDIS_CLIENT = AStrictRedisCluster(
        host=FI_REDIS_SERVER,
        port='6379',
        decode_responses=True,
        skip_full_coverage_check=True
    )
