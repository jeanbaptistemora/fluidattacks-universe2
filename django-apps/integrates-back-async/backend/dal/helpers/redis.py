
import redis
from __init__ import FI_REDIS_SERVER


REDIS_CLIENT = redis.StrictRedis(
    host=FI_REDIS_SERVER,
    port=6379,
    db=0,
    decode_responses=True)
