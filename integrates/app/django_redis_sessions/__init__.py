import redis
from rediscluster import RedisCluster
from redis.sentinel import Sentinel
import redis_sessions.session as session
import redis_sessions.settings as settings


SESSION_REDIS_CLUSTER = settings.SESSION_REDIS.get('cluster', None)


# pylint: disable=abstract-method
class SessionStore(session.SessionStore):
    def __init__(self, session_key=None):
        super(SessionStore, self).__init__(session_key)
        self.server = RedisServer(session_key).get()


class RedisServer(session.RedisServer):
    # pylint: disable=super-init-not-called
    def __init__(self, session_key):
        self.session_key = session_key
        self.connection_key = ''

        if settings.SESSION_REDIS_SENTINEL_LIST is not None:
            self.connection_type = 'sentinel'
        else:
            if settings.SESSION_REDIS_POOL is not None:
                server_key, server = \
                    self.get_server(session_key, settings.SESSION_REDIS_POOL)
                self.connection_key = str(server_key)
                settings.SESSION_REDIS_HOST = \
                    getattr(server, 'host', 'localhost')
                settings.SESSION_REDIS_PORT = getattr(server, 'port', 6379)
                settings.SESSION_REDIS_DB = getattr(server, 'db', 0)
                settings.SESSION_REDIS_PASSWORD = \
                    getattr(server, 'password', None)
                settings.SESSION_REDIS_URL = getattr(server, 'url', None)
                settings.SESSION_REDIS_UNIX_DOMAIN_SOCKET_PATH = \
                    getattr(server, 'unix_domain_socket_path', None)

            if settings.SESSION_REDIS_URL is not None:
                self.connection_type = 'redis_url'
            elif SESSION_REDIS_CLUSTER:
                self.connection_type = 'redis_cluster'
            elif settings.SESSION_REDIS_HOST is not None:
                self.connection_type = 'redis_host'
            elif settings.SESSION_REDIS_UNIX_DOMAIN_SOCKET_PATH is not None:
                self.connection_type = 'redis_unix_url'

        self.connection_key += self.connection_type

    def get(self):
        if self.connection_key in self.__redis:
            return self.__redis[self.connection_key]

        if self.connection_type == 'sentinel':
            self.__redis[self.connection_key] = Sentinel(
                settings.SESSION_REDIS_SENTINEL_LIST,
                socket_timeout=settings.SESSION_REDIS_SOCKET_TIMEOUT,
                retry_on_timeout=settings.SESSION_REDIS_RETRY_ON_TIMEOUT,
                db=getattr(settings, 'db', 0),
                password=getattr(settings, 'password', None)
            ).master_for(settings.SESSION_REDIS_SENTINEL_MASTER_ALIAS)

        elif self.connection_type == 'redis_url':
            self.__redis[self.connection_key] = redis.StrictRedis.from_url(
                settings.SESSION_REDIS_URL,
                socket_timeout=settings.SESSION_REDIS_SOCKET_TIMEOUT
            )
        elif self.connection_type == 'redis_host':
            self.__redis[self.connection_key] = redis.StrictRedis(
                host=settings.SESSION_REDIS_HOST,
                port=settings.SESSION_REDIS_PORT,
                socket_timeout=settings.SESSION_REDIS_SOCKET_TIMEOUT,
                retry_on_timeout=settings.SESSION_REDIS_RETRY_ON_TIMEOUT,
                db=settings.SESSION_REDIS_DB,
                password=settings.SESSION_REDIS_PASSWORD
            )
        elif self.connection_type == 'redis_cluster':
            self.__redis[self.connection_key] = RedisCluster(
                host=settings.SESSION_REDIS_HOST,
                port=settings.SESSION_REDIS_PORT,
                socket_timeout=settings.SESSION_REDIS_SOCKET_TIMEOUT,
                nodemanager_follow_cluster=True,
                skip_full_coverage_check=True
            )
        elif self.connection_type == 'redis_unix_url':
            unix_domain_socket_path = \
                settings.SESSION_REDIS_UNIX_DOMAIN_SOCKET_PATH
            self.__redis[self.connection_key] = redis.StrictRedis(
                unix_socket_path=unix_domain_socket_path,
                socket_timeout=settings.SESSION_REDIS_SOCKET_TIMEOUT,
                retry_on_timeout=settings.SESSION_REDIS_RETRY_ON_TIMEOUT,
                db=settings.SESSION_REDIS_DB,
                password=settings.SESSION_REDIS_PASSWORD,
            )

        return self.__redis[self.connection_key]
