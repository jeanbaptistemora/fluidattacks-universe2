{ integratesPkgs
, path
, ...
} @ _:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path integratesPkgs;
in
makeEntrypoint {
  arguments = {
    envKillPidListeningOnPort = import (path "/makes/utils/kill-pid-listening-on-port") path integratesPkgs;
    envRedisCli = "${integratesPkgs.redis}/bin/redis-cli";
    envRedisServer = "${integratesPkgs.redis}/bin/redis-server";
  };
  name = "integrates-server-redis";
  template = path "/makes/applications/integrates/server/redis/entrypoint.sh";
}
