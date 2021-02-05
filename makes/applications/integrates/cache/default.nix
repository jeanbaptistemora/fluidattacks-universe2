{ integratesPkgs
, applications
, path
, ...
} @ _:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path integratesPkgs;
in
makeEntrypoint {
  arguments = {
    envDone = applications."makes/done";
    envKillPidListeningOnPort = import (path "/makes/utils/kill-pid-listening-on-port") path integratesPkgs;
    envRedisCli = "${integratesPkgs.redis}/bin/redis-cli";
    envWait = applications."makes/wait";
    envRedisServer = "${integratesPkgs.redis}/bin/redis-server";
  };
  name = "integrates-cache";
  template = path "/makes/applications/integrates/cache/entrypoint.sh";
}
