{ integratesPkgs
, makeEntrypoint
, packages
, path
, ...
} @ _:
makeEntrypoint integratesPkgs {
  name = "integrates-cache";
  searchPaths = {
    envPaths = [
      integratesPkgs.redis
      packages."makes/done"
      packages."makes/kill-port"
      packages."makes/wait"
    ];
  };
  template = path "/makes/applications/integrates/cache/entrypoint.sh";
}
