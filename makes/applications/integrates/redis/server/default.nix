{ integratesPkgs
, outputs
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
    envWait = outputs.apps."makes/wait".program;
    envRedisServer = "${integratesPkgs.redis}/bin/redis-server";
  };
  name = "integrates-redis-server";
  template = path "/makes/applications/integrates/redis/server/entrypoint.sh";
}
