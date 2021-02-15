{ integratesPkgs
, applications
, makeEntrypoint
, packages
, path
, ...
} @ _:
makeEntrypoint integratesPkgs {
  arguments = {
    envDone = applications."makes/done";
    envRedisCli = "${integratesPkgs.redis}/bin/redis-cli";
    envWait = applications."makes/wait";
    envRedisServer = "${integratesPkgs.redis}/bin/redis-server";
  };
  name = "integrates-cache";
  searchPaths = {
    envPaths = [
      packages."makes/kill-port"
    ];
  };
  template = path "/makes/applications/integrates/cache/entrypoint.sh";
}
