{ integratesPkgs
, makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  name = "integrates-cache";
  searchPaths = {
    envPaths = [
      integratesPkgs.redis
      packages.makes.done
      packages.makes.kill-port
      packages.makes.wait
    ];
  };
  template = path "/makes/applications/integrates/cache/entrypoint.sh";
}
