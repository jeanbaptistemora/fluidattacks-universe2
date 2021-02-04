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
    envDone = outputs.apps."makes/done".program;
    envKillPidListeningOnPort = import (path "/makes/utils/kill-pid-listening-on-port") path integratesPkgs;
    envRedisCli = "${integratesPkgs.redis}/bin/redis-cli";
    envWait = outputs.apps."makes/wait".program;
    envRedisServer = "${integratesPkgs.redis}/bin/redis-server";
  };
  name = "integrates-cache";
  template = path "/makes/packages/integrates/cache/bin/entrypoint.sh";
}
