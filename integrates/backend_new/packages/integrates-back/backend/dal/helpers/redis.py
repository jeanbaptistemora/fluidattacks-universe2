
from aredis import (
    StrictRedis as AStrictRedis,
    StrictRedisCluster as AStrictRedisCluster,
)
from __init__ import FI_ENVIRONMENT, FI_REDIS_SERVER

CLIENT_CONFIG = {
    'host': FI_REDIS_SERVER,
    'port': 6379,
    'decode_responses': True,
    'max_connections': 64,
}
if FI_ENVIRONMENT == 'development':
    AREDIS_CLIENT = AStrictRedis(
        **CLIENT_CONFIG,
        db=0,
    )
else:
    AREDIS_CLIENT = AStrictRedisCluster(
        **CLIENT_CONFIG,
        skip_full_coverage_check=True,
    )
