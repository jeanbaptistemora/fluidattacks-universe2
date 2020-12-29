# Third party libraries
from aredis import (
    StrictRedisCluster as AStrictRedisCluster,
)

# Local libraries
from __init__ import (
    FI_REDIS_SERVER,
)

# Constants
AREDIS_CLIENT = AStrictRedisCluster(
    decode_responses=True,
    host=FI_REDIS_SERVER,
    max_connections=2048,
    port=6379,
    skip_full_coverage_check=True,
)
